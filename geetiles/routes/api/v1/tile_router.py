"""API ROUTER"""

import logging
import json

from flask import jsonify, Blueprint, redirect, request
from geetiles.routes.api import error
from geetiles.middleware import exist_mapid, get_layer, exist_tile, is_microservice_or_admin
from geetiles.services.redis_service import RedisService
from geetiles.services.storage_service import StorageService
import ee


tile_endpoints = Blueprint('tile_endpoints', __name__)


@tile_endpoints.route('/<layer>/expire-cache', strict_slashes=False, methods=['DELETE'])
@is_microservice_or_admin
def expire_cache(layer):
    """Expire cache tile layer Endpoint"""
    logging.info('[ROUTER]: Expire cache tile')
    RedisService.expire_layer(layer)
    StorageService.delete_folder(layer)
    return "", 200


@tile_endpoints.route('/<layer>/tile/gee/<z>/<x>/<y>', strict_slashes=False, methods=['GET'])
@exist_tile
@exist_mapid
@get_layer
def get_tile(layer, z, x, y, map_object=None, layer_obj=None):
    """Get tile Endpoint"""
    logging.info('[ROUTER]: Get tile')
    logging.info(map_object)
    try:
        if map_object is None:
            logging.debug('Generating mapid')
            layer_config = layer_obj.get('layerConfig')
            style_type = layer_config.get('body').get('styleType')
            image = None
            if 'isImageCollection' not in layer_config or not layer_config.get('isImageCollection'):
                image = ee.Image(layer_config.get('assetId'))
            else:
                position = layer_config.get('position')
                image_col = ee.ImageCollection(layer_config.get('assetId'))
                if 'filterDates' in layer_config:
                    dates = layer_config.get('filterDates')
                    image_col = image_col.filterDate(dates[0], dates[1])
                if position == 'first':
                    logging.info('Obtaining first')
                    image = ee.Image(image_col.sort('system:time_start', True).first())
                else:
                    logging.info('Obtaining last')
                    image = ee.Image(image_col.sort('system:time_start', False).first())
            
            if style_type == 'sld':
                style = layer_config.get('body').get('sldValue')
                map_object = image.sldStyle(style).getMapId()
            else:
                map_object = image.getMapId(layer_config.get('body'))

            logging.debug('Saving in cache')
            RedisService.set_layer_mapid(layer, map_object.get('mapid'), map_object.get('token'))
    except Exception as e:
        logging.error(str(e))
        return error(status=500, detail='Error generating tile: ' + str(e))
    try:
        url = ee.data.getTileUrl(map_object, int(x), int(y), int(z))
        storage_url = StorageService.upload_file(url, layer, map_object.get('mapid'), z, x, y)
    except Exception as e:
        logging.error(str(e))
        return error(status=404, detail='Tile Not Found')
    return redirect(storage_url)

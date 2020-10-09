"""API ROUTER"""

import logging
import os
import ee
from flask import Blueprint, redirect

from geetiles.middleware import get_layer, get_tile_from_cache, is_microservice
from geetiles.routes.api import error
from geetiles.services.redis_service import RedisService
from geetiles.services.storage_service import StorageService

LOGGER_LEVEL = os.environ.get('LOGGER_LEVEL', 'WARN').upper()
logging.basicConfig(level=LOGGER_LEVEL)

tile_endpoints = Blueprint('tile_endpoints', __name__)


@tile_endpoints.route('/gee/<layer>/expire-cache', strict_slashes=False, methods=['POST'])
@is_microservice
def expire_cache(layer):
    """Expire cache tile layer Endpoint"""
    logging.info('[tile_router - expire_cache]: Expire cache tile')
    logging.info('[tile_router - expire_cache]: Clearing Redis data')
    RedisService.expire_layer(layer)
    logging.info('[tile_router - expire_cache]: Redis data cleared, clearing Google Storage data')
    StorageService.delete_folder(layer)
    logging.info('[tile_router - expire_cache]: Tile cache cleared')
    return "", 200


@tile_endpoints.route('/<layer>/tile/gee/<z>/<x>/<y>', strict_slashes=False, methods=['GET'])
@get_tile_from_cache
@get_layer
def get_tile(layer, z, x, y, map_object=None, layer_obj=None):
    """Get tile Endpoint"""
    logging.info('[ROUTER]: Getting tile for layer {} and map_object {}'.format(layer, map_object))
    logging.info(map_object)
    try:
        layer_config = layer_obj.get('layerConfig')
        style_type = layer_config.get('body').get('styleType')
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

        logging.debug('get_tile - Saving in cache')
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

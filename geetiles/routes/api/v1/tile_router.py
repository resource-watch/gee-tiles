"""API ROUTER"""

import logging
import json

from flask import jsonify, Blueprint, redirect, request
from geetiles.routes.api import error
from geetiles.middleware import exist_mapid, get_layer, exist_tile
from geetiles.services.redis_service import RedisService
from geetiles.services.storage_service import StorageService
import ee


tile_endpoints = Blueprint('tile_endpoints', __name__)


@tile_endpoints.route('/<layer>/tile/<type>/<z>/<x>/<y>', strict_slashes=False, methods=['GET'])
@exist_tile
@exist_mapid
@get_layer
def get_tile(layer, type, z, x, y, map_object=None, layer_obj=None):
    """World Endpoint"""
    logging.info('[ROUTER]: Get tile')
    logging.info(map_object)
    if map_object is None:
        logging.debug('Generating mapid')
        style_type = layer_obj.get('layerConfig').get('body').get('styleType')
        image = layer_obj.get('layerConfig').get('assetId')
        if style_type == 'sld':
            style = layer_obj.get('layerConfig').get('body').get('sldValue')

            map_object = ee.Image(image).sldStyle(style).getMapId()
        else:
            map_object = ee.Image(image).getMapId(layer_obj.get('layerConfig').get('body'))

        logging.debug('Saving in cache')
        RedisService.set_layer_mapid(layer, map_object.get('mapid'), map_object.get('token'))

    try:
        url = ee.data.getTileUrl(map_object, int(x), int(y), int(z))
        storage_url = StorageService.upload_file(url, layer, z, x, y)
    except Exception as e:
        logging.error(str(e))
        return error(status=404, detail='Tile Not Found')

    return redirect(storage_url)

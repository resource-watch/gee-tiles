"""API ROUTER"""

import logging
import ee
import random
import os

from flask import jsonify, Blueprint, redirect, request
from ps.routes.api import error
from ps.middleware import exist_mapid, get_layer, exist_tile
from ps.services.redis_service import RedisService
import json
import CTRegisterMicroserviceFlask

from urllib.request import urlretrieve
from google.cloud import storage

tile_endpoints = Blueprint('tile_endpoints', __name__)


@tile_endpoints.route('/<layer>/tile/<type>/<z>/<x>/<y>', strict_slashes=False, methods=['GET'])
@exist_tile
@exist_mapid
@get_layer
def get_tile(layer, type, z, x, y, map_object=None, layer_obj=None):
    """World Endpoint"""
    logging.info('[ROUTER]: Get tile')
    logging.debug(layer_obj)
    if map_object == None:
        logging.debug('Generating mapid')
        style_type = layer_obj.get('layerConfig').get('body').get('styleType');
        if style_type == 'sld':
            style=layer_obj.get('layerConfig').get('body').get('sldValue')
            image = layer_obj.get('layerConfig').get('assetId')
            map_object = ee.Image(image).sldStyle(style).getMapId();
        # else:
            
        
        
        logging.debug('Saving in cache')
        RedisService.set_layer_mapid(layer, map_object.get('mapid'), map_object.get('token'))
        
    
    client = storage.Client()
    
    # .getMapId({'opacity':1, 'gain':3, 'bias': 5, 'gamma':1.1,format:'png'});
    
    
    logging.info('PAth '+ request.path)
    
    
    url = ee.data.getTileUrl(map_object, int(x), int(y), int(z))
    name = str(random.random())
    urlretrieve(url, name + '.png')

    bucket = client.get_bucket('gee-tiles')
    blob = bucket.blob('/' + layer + '/' + z + '/' +x + '/' +y + '/' + 'tile.png')
    with open(name + '.png', 'rb') as my_file:
        blob.upload_from_file(my_file)
        blob.make_public()
        RedisService.set(request.path,blob.public_url )
        os.remove(name + '.png')
        return redirect(blob.public_url)
    

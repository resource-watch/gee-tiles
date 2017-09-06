import logging

from functools import wraps
from flask import request, redirect

from ps.services.redis_service import RedisService
from ps.services.layer_service import LayerService


def exist_tile(func):
    """Get geodata"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = RedisService.get(request.path)
        if url == None:
            return func(*args, **kwargs)
        else:
            return redirect(url)
    return wrapper
def exist_mapid(func):
    """Get geodata"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        layer = kwargs['layer']
        logging.debug('Checking if exist in cache layer ' + layer)
        kwargs["map_object"] = RedisService.check_layer_mapid(layer)
        return func(*args, **kwargs)
    return wrapper

def get_layer(func):
    """Get geodata"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs['map_object'] == None:
            layer = kwargs['layer']         
            logging.debug('Getting layer ' + layer)
            kwargs["layer_obj"] = LayerService.get(layer)
        return func(*args, **kwargs)
    return wrapper

import logging
import os
import json
from functools import wraps

from flask import request, redirect

from geetiles.errors import LayerNotFound
from geetiles.routes.api import error
from geetiles.services.layer_service import LayerService
from geetiles.services.redis_service import RedisService

LOGGER_LEVEL = os.environ.get('LOGGER_LEVEL', 'WARN').upper()
logging.basicConfig(level=LOGGER_LEVEL)


def get_tile_from_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug('get_tile_from_cache - requesting {} from Redis cache'.format(request.path))
        url = RedisService.get(request.path)
        if url is None:
            logging.debug('get_tile_from_cache - no cached tile found, loading from GEE')
            return func(*args, **kwargs)
        else:
            logging.debug('get_tile_from_cache - tile found in redis, returning cached value')
            return redirect(url)

    return wrapper


def is_microservice(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug("Checking microservice user")
        logged_user = json.loads(request.args.get("loggedUser", '{}'))
        if logged_user.get("id") == "microservice":
            logging.debug("is microservice")
            return func(*args, **kwargs)
        else:
            return error(status=403, detail="Not authorized")

    return wrapper


def get_layer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            layer = kwargs['layer']
            logging.debug("get_layer - loading layer {} from LayerService".format(layer))
            kwargs["layer_obj"] = LayerService.get(layer, request.headers.get("x-api-key"))
            return func(*args, **kwargs)
        except LayerNotFound as e:
            logging.error("get_layer - LayerNotFound - {}".format(e.message))
            return error(status=404, detail=e.message)
        except Exception as e:
            logging.error("get_layer - Exception - {}".format(e.message))
            return error(detail='Generic error')

    return wrapper

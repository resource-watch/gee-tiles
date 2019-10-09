import logging
from functools import wraps

from flask import request, redirect

from geetiles.errors import LayerNotFound
from geetiles.routes.api import error
from geetiles.services.layer_service import LayerService
from geetiles.services.redis_service import RedisService


def exist_tile(func):
    """Get geodata"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        url = RedisService.get(request.path)
        if url is None:
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


def is_microservice_or_admin(func):
    """Get geodata"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug("Checking microservice user")
        logged_user = request.json.get("loggedUser", None)
        if (logged_user.get("id") == "microservice") or (logged_user.get("role") == "ADMIN"):
            logging.debug("is microservice or admin")
            return func(*args, **kwargs)
        else:
            return error(status=403, detail="Not authorized")

    return wrapper


def get_layer(func):
    """Get geodata"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if kwargs['map_object'] is None:
                layer = kwargs['layer']
                logging.debug('Getting layer ' + layer)
                kwargs["layer_obj"] = LayerService.get(layer)
            return func(*args, **kwargs)
        except LayerNotFound as e:
            return error(status=404, detail=e.message)
        except Exception as e:
            return error(detail='Generic error')

    return wrapper

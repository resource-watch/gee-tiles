""" Redis service """

import logging
import os
import redis

from geetiles.config import SETTINGS

LOGGER_LEVEL = os.environ.get('LOGGER_LEVEL', 'WARN').upper()

redis_connection = redis.StrictRedis.from_url(url=SETTINGS.get('redis').get('url'))


class RedisService(object):

    @staticmethod
    def get(layer):
        text = redis_connection.get(layer)
        if text is not None:
            return text
        return None

    @staticmethod
    def set(key, value):
        return redis_connection.set(key, value)

    @staticmethod
    def expire_layer(layer):
        for key in redis_connection.scan_iter("*" + layer + "*"):
            logging.debug('[RedisService - expire_layer]: Deleting key {}'.format(key))
            redis_connection.delete(key)

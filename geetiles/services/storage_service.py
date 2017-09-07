""" Storage service """
import logging
import random
import os
import uuid

from flask import request
from urllib.request import urlretrieve
from google.cloud import storage

from geetiles.services.redis_service import RedisService

client = storage.Client()

class StorageService(object):
    
    @staticmethod
    def upload_file(url, layer, z, x, y):
        name = str(uuid.uuid4()) + '.png'
        urlretrieve(url, name)

        bucket = client.get_bucket('gee-tiles')
        blob = bucket.blob('/' + layer + '/' + z + '/' +x + '/' +y + '/' + 'tile.png')
        with open(name, 'rb') as my_file:
            blob.upload_from_file(my_file)
            blob.make_public()
            RedisService.set(request.path,blob.public_url )
            os.remove(name)
            return blob.public_url

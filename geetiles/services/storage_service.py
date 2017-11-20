""" Storage service """


import os
import uuid
import logging

from flask import request
from urllib.request import urlretrieve
from google.cloud import storage

from geetiles.services.redis_service import RedisService

client = storage.Client()


class StorageService(object):

    @staticmethod
    def delete_folder(layer): 
        bucket = client.get_bucket('gee-tiles')
        #blob = bucket.blob(layer+"/0/0/0/tile.png")
        list = bucket.list_blobs(prefix=layer)
        for blob in list:
            logging.debug(blob)
            blob.delete()
        logging.debug("Folder removed")

    @staticmethod
    def upload_file(url, layer, map_id z, x, y):
        name = str(uuid.uuid4()) + '.png'
        urlretrieve(url, name)

        bucket = client.get_bucket('gee-tiles')
        blob = bucket.blob(layer + '/' + z + '/' + x + '/' + y + '/' + 'tile_' + map_id + '.png')
        with open(name, 'rb') as my_file:
            blob.upload_from_file(my_file)
            blob.make_public()
            RedisService.set(request.path, blob.public_url)
            os.remove(name)
            return blob.public_url

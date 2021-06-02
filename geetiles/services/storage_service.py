""" Storage service """

import logging
import os
from uuid import uuid4 as uuid
from urllib.request import urlretrieve

from flask import request
from google.cloud.storage import Client as storageClient
from geetiles.services.redis_service import RedisService


class StorageService(object):

    @staticmethod
    def delete_folder(layer):
        storage_client = storageClient()
        bucket = storage_client.get_bucket('gee-tiles')

        list = bucket.list_blobs(prefix=layer)
        for blob in list:
            logging.debug(blob)
            blob.delete()
        logging.debug("Folder removed")

    @staticmethod
    def upload_file(url, layer, map_id, z, x, y):
        name = str(uuid()) + '.png'
        urlretrieve(url, name)

        storage_client = storageClient()
        bucket = storage_client.get_bucket('gee-tiles')
        blob = bucket.blob(layer + '/' + z + '/' + x + '/' + y + '/' + 'tile_' + map_id + '.png')
        with open(name, 'rb') as my_file:
            blob.upload_from_file(my_file)
            blob.make_public()
            RedisService.set(request.path, blob.public_url)
            os.remove(name)
            return blob.public_url

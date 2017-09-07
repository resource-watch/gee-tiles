""" Layer service """
import logging
import redis
import json


from geetiles.errors import LayerNotFound
from CTRegisterMicroserviceFlask import request_to_microservice

class LayerService(object):
    
    @staticmethod
    def execute(config):
        try:
            response = request_to_microservice(config)
            if not response or response.get('errors'):
                raise LayerNotFound
            layer = response.get('data', None).get('attributes', None)
        except Exception as e:
            raise LayerNotFound(message=str(e))
        return layer

    @staticmethod
    def get(layer):
        config = {
            'uri': '/layer/'+layer,
            'method': 'GET'
        }
        return LayerService.execute(config)

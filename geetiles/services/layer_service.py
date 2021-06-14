""" Layer service """

from RWAPIMicroservicePython import request_to_microservice

from geetiles.errors import LayerNotFound


class LayerService(object):

    @staticmethod
    def execute(config):
        response = request_to_microservice(config)
        if not response or response.get('errors'):
            raise LayerNotFound(message='Layer not found')

        layer = response.get('data', None).get('attributes', None)
        return layer

    @staticmethod
    def get(layer):
        config = {
            'uri': '/v1/layer/' + layer,
            'method': 'GET'
        }
        return LayerService.execute(config)

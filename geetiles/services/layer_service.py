""" Layer service """

from RWAPIMicroservicePython import request_to_microservice

from geetiles.errors import LayerNotFound


class LayerService(object):
    @staticmethod
    def execute(uri, api_key):
        response = request_to_microservice(uri=uri, api_key=api_key, method="GET")
        if not response or response.get("errors"):
            raise LayerNotFound(message="Layer not found")

        layer = response.get("data", None).get("attributes", None)
        return layer

    @staticmethod
    def get(layer, api_key):
        uri = f"/v1/layer/{layer}"

        return LayerService.execute(uri, api_key)

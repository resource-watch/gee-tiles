import os
from unittest.mock import patch, MagicMock

import pytest
import requests_mock

import geetiles
from geetiles.services.redis_service import RedisService

LAYER = {
   "data":{
      "id":"e8f9a96a-0a2c-4cf9-b904-36531f23a8b2",
      "type":"layer",
      "attributes":{
         "name":"TML_sld_layer",
         "slug":"TML_sld_layer",
         "dataset":"e9e91ed6-22b0-4280-8710-34589b0b1336",
         "description":"",
         "application":[
            "rw"
         ],
         "iso":[
            
         ],
         "provider":"gee",
         "userId":"58fde4354eecd9073107af0f",
         "default":True,
         "protected":False,
         "published":True,
         "env":"preproduction",
         "layerConfig":{
            "body":{
               "sldValue":"<RasterSymbolizer><ColorMap extended=\"false\" type=\"intervals\"><ColorMapEntry color=\"#ebf5eb\" quantity=\"0\" label=\"0-20\" opacity=\"0\"/><ColorMapEntry color=\"#ebf5eb\" quantity=\"20\" label=\"0-20\"/><ColorMapEntry color=\"#a0d796\" quantity=\"30\" label=\"20-40\"/><ColorMapEntry color=\"#68b869\" quantity=\"40\" label=\"20-40\"/><ColorMapEntry color=\"#68b869\" quantity=\"50\" label=\"40-60\"/><ColorMapEntry color=\"#2c8e4a\" quantity=\"60\" label=\"40-60\"/><ColorMapEntry color=\"#2c8e4a\" quantity=\"70\" label=\"60-80\"/><ColorMapEntry color=\"#0f803a\" quantity=\"80\" label=\"80-100\"/><ColorMapEntry color=\"#0f803a\" quantity=\"90\" label=\"80-100\"/><ColorMapEntry color=\"#0f803a\" quantity=\"100\" label=\"80-100\"/><ColorMapEntry color=\"#000000\" quantity=\"255\" label=\"255\" opacity=\"0\"/></ColorMap></RasterSymbolizer>",
               "styleType":"sld"
            },
            "assetId":"projects/wri-datalab/TML",
            "isImageCollection":True,
            "provider":"gee",
            "position":"mosaic"
         },
         "legendConfig":{
            "type":"choropleth",
            "items":[
               {
                  "name":"0-20",
                  "color":"#edf8e9",
                  "id":0
               },
               {
                  "name":"20-40",
                  "color":"#a0d796",
                  "id":1
               },
               {
                  "name":"40-60",
                  "color":"#68b869",
                  "id":2
               },
               {
                  "name":"60-80",
                  "color":"#2c8e49",
                  "id":3
               },
               {
                  "name":"80-100",
                  "color":"#076f2f",
                  "id":4
               }
            ]
         },
         "interactionConfig":{
            
         },
         "applicationConfig":{
            
         },
         "staticImageConfig":{
            
         },
         "createdAt":"2021-10-14T13:42:22.034Z",
         "updatedAt":"2021-10-14T13:42:22.034Z"
      }
   }
}


@pytest.fixture
def client():
    app = geetiles.app
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@patch("ee.data.getTileUrl")
@patch("ee.Image")
@patch("geetiles.services.storage_service.uuid")
@patch("geetiles.services.storage_service.storageClient")
@requests_mock.mock(kw='mocker')
def test_get_tile_mosaic_cold_cache(storageClient, uuid, Image, getTileUrl, client, mocker):
    # Populate a bunch of internal mocks to avoid calls to actual GEE servers
    uuid.return_value = os.getcwd()+'/tests/tile'
    Image.return_value.sldStyle.return_value.getMapId.return_value = {
                                'mapid': 'projects/earthengine-legacy/maps/abcd-efgh',
                                'token': '', 'tile_fetcher': MagicMock(), 'image': MagicMock()
    }

    getTileUrl.return_value = 'https://picsum.photos/200/300'
    bucket = storageClient().get_bucket
    blob = bucket().blob
    blob().public_url = 'https://my-tile.server/1234/4/7/6.png'

    # Mock request to layer MS
    get_layer = mocker.get(os.getenv('GATEWAY_URL') + '/v1/layer/1234', status_code=200, json=LAYER)

    # Clean Redis cache
    RedisService.expire_layer('1234')

    # Call to the actual endpoint
    response = client.get('/api/v1/layer/1234/tile/gee/4/7/6')

    uuid.assert_called()
    Image().sldStyle.assert_called()
    Image().sldStyle().getMapId.assert_called()
    getTileUrl.assert_called()

    bucket.assert_called_with('gee-tiles')

    blob.assert_called_with(
        '1234/4/7/6/tile_projects/earthengine-legacy/maps/abcd-efgh.png')
    blob().upload_from_file.assert_called()
    blob().make_public.assert_called()

    assert response.headers['Location'] == 'https://my-tile.server/1234/4/7/6.png'
    assert response.status_code == 302

    assert RedisService.get('/api/v1/layer/1234/tile/gee/4/7/6') == b'https://my-tile.server/1234/4/7/6.png'

    assert get_layer.called
    assert get_layer.call_count == 1


def test_get_tile_mosaic_warm_cache(client):
    # Populate Redis cache
    RedisService.set('/api/v1/layer/1234/tile/gee/4/7/6', b'https://my-tile.server/1234/4/7/6.png')

    # Call to the actual endpoint
    response = client.get('/api/v1/layer/1234/tile/gee/4/7/6')

    assert response.headers['Location'] == 'https://my-tile.server/1234/4/7/6.png'
    assert response.status_code == 302

    assert RedisService.get('/api/v1/layer/1234/tile/gee/4/7/6') == b'https://my-tile.server/1234/4/7/6.png'

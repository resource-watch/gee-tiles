import os
from unittest.mock import patch, MagicMock

import pytest
import requests_mock

import geetiles
from geetiles.services.redis_service import RedisService

LAYER = {
    "data": {
        "id": "d787d894-f7af-47c4-af0f-0849b06686ee",
        "type": "layer",
        "attributes": {
            "name": "2015 Accessibility to Cities",
            "slug": "Travel-Time-to-Major-Cities_1",
            "dataset": "ccbcaf7b-1619-4298-8275-b135d1e8e04e",
            "description": "Time it takes to travel to the nearest city in 2015. Units are minutes, hours, days, and months.",
            "application": [
                "rw"
            ],
            "iso": [],
            "provider": "gee",
            "userId": "5980838ae24e6a1dae3dd446",
            "default": True,
            "protected": False,
            "published": True,
            "env": "production",
            "layerConfig": {
                "body": {
                    "sldValue": "<RasterSymbolizer>    <ColorMap  type=\"ramp\" extended=\"false\" >      '<ColorMapEntry color=\"#FFFFFF\" quantity=\"0\" opacity=\"1\" />' +    '<ColorMapEntry color=\"#C0F09C\" quantity=\"60\" opacity=\"1\" />' +    '<ColorMapEntry color=\"#E3DA64\" quantity=\"120\"  />' +  '<ColorMapEntry color=\"#D16638\" quantity=\"180\"  />' +    '<ColorMapEntry color=\"#BA2D2F\" quantity=\"360\" />' +   '<ColorMapEntry color=\"#A11F4A\" quantity=\"720\"  />' +    '<ColorMapEntry color=\"#730D6F\" quantity=\"1440\"  />' +    '<ColorMapEntry color=\"#0D0437\" quantity=\"20160\"  />' +  '<ColorMapEntry color=\"#00030F\" quantity=\"41556\"  />' +    </ColorMap></RasterSymbolizer>",
                    "styleType": "sld",
                    "url": "https://staging-api.globalforestwatch.org/v1/layer/d787d894-f7af-47c4-af0f-0849b06686ee/tile/gee/{z}/{x}/{y}"
                },
                "assetId": "Oxford/MAP/accessibility_to_cities_2015_v1_0",
                "type": "gee"
            },
            "legendConfig": {
                "items": [
                    {
                        "name": "0 h",
                        "color": "#FFFFFF"
                    },
                    {
                        "color": "#C0F09C",
                        "name": "1 h"
                    },
                    {
                        "color": "#E3DA64",
                        "name": "2 h"
                    },
                    {
                        "color": "#D16638",
                        "name": "3 h"
                    },
                    {
                        "color": "#BA2D2F",
                        "name": "6 h"
                    },
                    {
                        "color": "#A11F4A",
                        "name": "12 h"
                    },
                    {
                        "color": "#730D6F",

                        "name": "1 d"
                    },
                    {
                        "color": "#0D0437",
                        "name": "14 d"
                    },
                    {
                        "color": "#00030F",
                        "name": "1 m"
                    }
                ],
                "type": "choropleth"
            },
            "interactionConfig": {},
            "applicationConfig": {},
            "staticImageConfig": {},
            "createdAt": "2020-02-12T11:19:24.568Z",
            "updatedAt": "2020-02-12T12:18:00.198Z"
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
def test_get_tile_cold_cache(storageClient, uuid, Image, getTileUrl, client, mocker):
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


def test_get_tile_warm_cache(client):
    # Populate Redis cache
    RedisService.set('/api/v1/layer/1234/tile/gee/4/7/6', b'https://my-tile.server/1234/4/7/6.png')

    # Call to the actual endpoint
    response = client.get('/api/v1/layer/1234/tile/gee/4/7/6')

    assert response.headers['Location'] == 'https://my-tile.server/1234/4/7/6.png'
    assert response.status_code == 302

    assert RedisService.get('/api/v1/layer/1234/tile/gee/4/7/6') == b'https://my-tile.server/1234/4/7/6.png'

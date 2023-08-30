import os
from unittest.mock import patch, MagicMock

import requests_mock
from RWAPIMicroservicePython.test_utils import mock_request_validation

from geetiles.services.redis_service import RedisService

from tests.fixtures import TML_LAYER as LAYER


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
    get_layer = mocker.get(
        os.getenv('GATEWAY_URL') + '/v1/layer/1234',
        status_code=200,
        json=LAYER,
        request_headers={'x-api-key': 'api-key-test'}
    )
    mock_request_validation(
        mocker,
        microservice_token=os.getenv("MICROSERVICE_TOKEN"),
    )
    # Clean Redis cache
    RedisService.expire_layer('1234')

    # Call to the actual endpoint
    response = client.get(
        '/api/v1/layer/1234/tile/gee/4/7/6', headers={'x-api-key': 'api-key-test'}
    )

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


@requests_mock.mock(kw='mocker')
def test_get_tile_mosaic_warm_cache(client, mocker):
    # Populate Redis cache
    RedisService.set('/api/v1/layer/1234/tile/gee/4/7/6', b'https://my-tile.server/1234/4/7/6.png')

    # Call to the actual endpoint
    mock_request_validation(
        mocker,
        microservice_token=os.getenv("MICROSERVICE_TOKEN"),
    )
    # Call to the actual endpoint
    response = client.get(
        '/api/v1/layer/1234/tile/gee/4/7/6', headers={'x-api-key': 'api-key-test'}
    )
    assert response.headers['Location'] == 'https://my-tile.server/1234/4/7/6.png'
    assert response.status_code == 302

    assert RedisService.get('/api/v1/layer/1234/tile/gee/4/7/6') == b'https://my-tile.server/1234/4/7/6.png'

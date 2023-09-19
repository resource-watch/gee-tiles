import json
import os

import requests_mock
from unittest.mock import patch, MagicMock
from RWAPIMicroservicePython.test_utils import mock_request_validation

from geetiles.services.redis_service import RedisService
from tests.fixtures import USERS

@patch("geetiles.services.storage_service.storageClient")
@requests_mock.mock(kw='mocker')
def test_expire_cache_as_microservice(storageClient, client, mocker):
    # Deleting cache as a MICROSERVICE-based user should return ...

    RedisService.set('/api/v1/layer/testLayerId/tile/gee/11/1051/726', b'https://my-tile.server/1234/4/7/6.png')

    bucket = storageClient().get_bucket
    list_blobs = bucket().list_blobs
    blob_from_list = MagicMock()
    list_blobs.return_value = [blob_from_list]

    get_user_data_calls = mock_request_validation(
        mocker,
        microservice_token=os.getenv("MICROSERVICE_TOKEN"),
        user=USERS["MICROSERVICE"],
    )

    response = client.delete(
        '/api/v1/layer/gee/testLayerId/expire-cache',
        headers={
            'Authorization': 'Bearer abcd',
            'x-api-key': 'api-key-test'
        }
    )
    assert response.data == b''
    assert response.status_code == 200
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1
    bucket.assert_called_with('gee-tiles')
    list_blobs.assert_called_with(prefix='testLayerId')
    blob_from_list.delete.assert_called()


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_admin(client, mocker):
    # Deleting cache as a ADMIN-based user should return a 403
    get_user_data_calls = mock_request_validation(
        mocker,
        microservice_token=os.getenv("MICROSERVICE_TOKEN"),
        user=USERS["ADMIN"],
    )

    response = client.delete(
        '/api/v1/layer/gee/testLayerId/expire-cache',
        headers={
            'Authorization': 'Bearer abcd',
            'x-api-key': 'api-key-test'
        }
    )
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_manager(client, mocker):
    # Deleting cache as a MANAGER-based user should return a 403
    get_user_data_calls = mock_request_validation(
        mocker,
        microservice_token=os.getenv("MICROSERVICE_TOKEN"),
        user=USERS["MANAGER"],
    )

    response = client.delete(
        '/api/v1/layer/gee/testLayerId/expire-cache',
        headers={
            'Authorization': 'Bearer abcd',
            'x-api-key': 'api-key-test'
        }
    )
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_user(client, mocker):
    # Deleting cache as a USER-based user should return a 403
    get_user_data_calls = mock_request_validation(
        mocker,
        microservice_token=os.getenv("MICROSERVICE_TOKEN"),
        user=USERS["USER"],
    )

    response = client.delete(
        '/api/v1/layer/gee/testLayerId/expire-cache',
        headers={
            'Authorization': 'Bearer abcd',
            'x-api-key': 'api-key-test'
        }
    )
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_anon(client, mocker):
    # Deleting cache as a USER-based user should return a 403
    get_user_data_calls = mock_request_validation(
        mocker,
        microservice_token=os.getenv("MICROSERVICE_TOKEN"),
    )

    response = client.delete(
        '/api/v1/layer/gee/testLayerId/expire-cache',
        headers={'x-api-key': 'api-key-test'}
        )
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403
    assert get_user_data_calls.call_count == 1

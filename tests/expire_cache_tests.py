import json
import os

import pytest
import requests_mock
import geetiles
from unittest.mock import patch, MagicMock
from geetiles.services.redis_service import RedisService

USERS = {
    "ADMIN": {
        "id": '1a10d7c6e0a37126611fd7a7',
        "role": 'ADMIN',
        "provider": 'local',
        "email": 'user@control-tower.org',
        "name": 'John Admin',
        "extraUserData": {
            "apps": [
                'rw',
                'gfw',
                'gfw-climate',
                'prep',
                'aqueduct',
                'forest-atlas',
                'data4sdgs'
            ]
        }
    },
    "MANAGER": {
        "id": '1a10d7c6e0a37126611fd7a7',
        "role": 'MANAGER',
        "provider": 'local',
        "email": 'user@control-tower.org',
        "extraUserData": {
            "apps": [
                'rw',
                'gfw',
                'gfw-climate',
                'prep',
                'aqueduct',
                'forest-atlas',
                'data4sdgs'
            ]
        }
    },
    "USER": {
        "id": '1a10d7c6e0a37126611fd7a7',
        "role": 'USER',
        "provider": 'local',
        "email": 'user@control-tower.org',
        "extraUserData": {
            "apps": [
                'rw',
                'gfw',
                'gfw-climate',
                'prep',
                'aqueduct',
                'forest-atlas',
                'data4sdgs'
            ]
        }
    },
    "MICROSERVICE": {
        "id": 'microservice'
    },
}


@pytest.fixture
def client():
    app = geetiles.app
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@patch("geetiles.services.storage_service.storageClient")
@requests_mock.mock(kw='mocker')
def test_expire_cache_as_microservice(storageClient, client, mocker):
    # Deleting cache as a MICROSERVICE-based user should return ...

    RedisService.set('/api/v1/layer/testLayerId/tile/gee/11/1051/726', b'https://my-tile.server/1234/4/7/6.png')

    bucket = storageClient().get_bucket
    list_blobs = bucket().list_blobs
    blob_from_list = MagicMock()
    list_blobs.return_value = [blob_from_list]

    get_user_data_calls = mocker.get(os.getenv('GATEWAY_URL') + '/auth/user/me', status_code=200, json=USERS['MICROSERVICE'])

    response = client.delete('/api/v1/layer/gee/testLayerId/expire-cache', headers={'Authorization': 'Bearer abcd'})
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
    get_user_data_calls = mocker.get(os.getenv('GATEWAY_URL') + '/auth/user/me', status_code=200, json=USERS['ADMIN'])

    response = client.delete('/api/v1/layer/gee/testLayerId/expire-cache', headers={'Authorization': 'Bearer abcd'})
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_manager(client, mocker):
    # Deleting cache as a MANAGER-based user should return a 403
    get_user_data_calls = mocker.get(os.getenv('GATEWAY_URL') + '/auth/user/me', status_code=200, json=USERS['MANAGER'])

    response = client.delete(
        '/api/v1/layer/gee/testLayerId/expire-cache', headers={'Authorization': 'Bearer abcd'})
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_user(client, mocker):
    # Deleting cache as a USER-based user should return a 403
    get_user_data_calls = mocker.get(os.getenv('GATEWAY_URL') + '/auth/user/me', status_code=200, json=USERS['USER'])

    response = client.delete('/api/v1/layer/gee/testLayerId/expire-cache', headers={'Authorization': 'Bearer abcd'})
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_anon(client, mocker):
    # Deleting cache as a USER-based user should return a 403
    get_user_data_calls = mocker.get(os.getenv('GATEWAY_URL') + '/auth/user/me', status_code=200, json=USERS['USER'])

    response = client.delete('/api/v1/layer/gee/testLayerId/expire-cache')
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403
    assert get_user_data_calls.call_count == 0

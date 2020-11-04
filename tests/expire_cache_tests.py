import json

import pytest
import requests_mock

import geetiles

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

}


@pytest.fixture
def client():
    app = geetiles.app
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_admin(client, mocker):
    # Deleting cache as a ADMIN-based user should return a 403

    response = client.post('/api/v1/layer/gee/testLayerId/expire-cache', json=dict(loggedUser=USERS['ADMIN']))
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_manager(client, mocker):
    # Deleting cache as a MANAGER-based user should return a 403

    response = client.post(
        '/api/v1/layer/gee/testLayerId/expire-cache', json=dict(loggedUser=USERS['MANAGER']))
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_user(client, mocker):
    # Deleting cache as a USER-based user should return a 403

    response = client.post('/api/v1/layer/gee/testLayerId/expire-cache', json=dict(loggedUser=USERS['USER']))
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403

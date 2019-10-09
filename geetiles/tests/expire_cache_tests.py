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
    # Deleting cache as an ADMIN-based user should succeed

    mocker.post(
        'https://accounts.google.com/o/oauth2/token',
        json={
            'access_token': "fakeToken",
            "expires_in": 3600, "token_type": "Bearer"}
    )

    mocker.get('https://www.googleapis.com/storage/v1/b/gee-tiles?projection=noAcl',
               json={"kind": "storage#bucket", "id": "gee-tiles",
                     "selfLink": "https://www.googleapis.com/storage/v1/b/gee-tiles", "projectNumber": "123456",
                     "name": "gee-tiles", "timeCreated": "2017-09-06T16:55:16.193Z",
                     "updated": "2018-02-05T11:12:48.289Z", "metageneration": "2", "location": "US",
                     "locationType": "multi-region", "cors": [
                       {"origin": ["*"], "method": ["GET", "HEAD", "DELETE"], "responseHeader": ["Content-Type"],
                        "maxAgeSeconds": 3600}], "storageClass": "MULTI_REGIONAL", "etag": "CAI="})

    mocker.get('https://www.googleapis.com/storage/v1/b/gee-tiles/o?projection=noAcl&prefix=testLayerId',
               json={'kind': 'storage#objects', 'items': [{'kind': 'storage#object',
                                                           'id': 'gee-tiles/testLayerId/9/169/283/tile_854ffa01c65fbe214c1587f9308e77a6.png/1522853136643054',
                                                           'selfLink': 'https://www.googleapis.com/storage/v1/b/gee-tiles/o/testLayerId%2F9%2F169%2F283%2Ftile_854ffa01c65fbe214c1587f9308e77a6.png',
                                                           'name': 'testLayerId/9/169/283/tile_854ffa01c65fbe214c1587f9308e77a6.png',
                                                           'bucket': 'gee-tiles', 'generation': '1522853136643054',
                                                           'metageneration': '2',
                                                           'contentType': 'application/octet-stream',
                                                           'storageClass': 'MULTI_REGIONAL', 'size': '34199',
                                                           'md5Hash': 'Mlp3RxXNXA2KtN8Oc2Lgdw==',
                                                           'mediaLink': 'https://www.googleapis.com/download/storage/v1/b/gee-tiles/o/testLayerId%2F9%2F169%2F283%2Ftile_854ffa01c65fbe214c1587f9308e77a6.png?generation=1522853136643054&alt=media',
                                                           'crc32c': 'kwKCGw==', 'etag': 'CO7nhILuoNoCEAI=',
                                                           'timeCreated': '2018-04-04T14:45:36.600Z',
                                                           'updated': '2018-04-04T14:45:36.885Z',
                                                           'timeStorageClassUpdated': '2018-04-04T14:45:36.600Z'},
                                                          {'kind': 'storage#object',
                                                           'id': 'gee-tiles/testLayerId/9/169/284/tile_854ffa01c65fbe214c1587f9308e77a6.png/1522853136686208',
                                                           'selfLink': 'https://www.googleapis.com/storage/v1/b/gee-tiles/o/testLayerId%2F9%2F169%2F284%2Ftile_854ffa01c65fbe214c1587f9308e77a6.png',
                                                           'name': 'testLayerId/9/169/284/tile_854ffa01c65fbe214c1587f9308e77a6.png',
                                                           'bucket': 'gee-tiles', 'generation': '1522853136686208',
                                                           'metageneration': '2',
                                                           'contentType': 'application/octet-stream',
                                                           'storageClass': 'MULTI_REGIONAL', 'size': '32750',
                                                           'md5Hash': 'GP2kzks/qwzISVHQTCHPzg==',
                                                           'mediaLink': 'https://www.googleapis.com/download/storage/v1/b/gee-tiles/o/testLayerId%2F9%2F169%2F284%2Ftile_854ffa01c65fbe214c1587f9308e77a6.png?generation=1522853136686208&alt=media',
                                                           'crc32c': '4DvHHw==', 'etag': 'CIC5h4LuoNoCEAI=',
                                                           'timeCreated': '2018-04-04T14:45:36.645Z',
                                                           'updated': '2018-04-04T14:45:36.981Z',
                                                           'timeStorageClassUpdated': '2018-04-04T14:45:36.645Z'}]})

    mocker.delete(
        'https://www.googleapis.com/storage/v1/b/gee-tiles/o/testLayerId%2F9%2F169%2F283%2Ftile_854ffa01c65fbe214c1587f9308e77a6.png?generation=1522853136643054',
        status_code=204
    )

    mocker.delete(
        'https://www.googleapis.com/storage/v1/b/gee-tiles/o/testLayerId%2F9%2F169%2F284%2Ftile_854ffa01c65fbe214c1587f9308e77a6.png?generation=1522853136686208',
        status_code=204
    )

    response = client.post('/api/v1/layer/testLayerId/expire-cache', json=dict(loggedUser=USERS['ADMIN']))
    assert response.data == b''
    assert response.status_code == 200


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_manager(client, mocker):
    # Deleting cache as a MANAGER-based user should return a 403

    response = client.post(
        '/api/v1/layer/testLayerId/expire-cache', json=dict(loggedUser=USERS['MANAGER']))
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403


@requests_mock.mock(kw='mocker')
def test_expire_cache_as_user(client, mocker):
    # Deleting cache as a USER-based user should return a 403

    response = client.post('/api/v1/layer/testLayerId/expire-cache', json=dict(loggedUser=USERS['USER']))
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403

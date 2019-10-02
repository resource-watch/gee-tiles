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
    }
}


@pytest.fixture
def client():
    app = geetiles.app
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@requests_mock.mock(kw='mocker')
def test_expire_cache(client, mocker):
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
               json={'kind': 'storage#objects'})

    response = client.delete('/api/v1/layer/testLayerId/expire-cache?loggedUser={}'.format(json.dumps(USERS['ADMIN'])))
    assert response.data == b''
    assert response.status_code == 200

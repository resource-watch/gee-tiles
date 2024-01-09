"""-"""

import os

from geetiles.utils.files import BASE_DIR

SETTINGS = {
    'logging': {
        'level': 'DEBUG'
    },
    'service': {
        'name': 'Google Earth Engine Tiles',
        'port': os.getenv('PORT')
    },
    'redis': {
        'url': os.getenv('REDIS_URL')
    },
    'gee': {
        'service_account': os.getenv('EE_ACCOUNT'),
        'privatekey_file': BASE_DIR + '/privatekey.json',
    }
}

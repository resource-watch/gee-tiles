"""CONFIG MODULE"""

import os

from geetiles.config import base, staging, prod, test

SETTINGS = base.SETTINGS

if os.getenv('ENVIRONMENT') == 'staging':
    SETTINGS.update(staging.SETTINGS)

if os.getenv('ENVIRONMENT') == 'prod':
    SETTINGS.update(prod.SETTINGS)

if os.getenv('ENVIRONMENT') == 'test':
    SETTINGS.update(test.SETTINGS)

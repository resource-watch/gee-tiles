"""The API MODULE"""

import logging
import os

import ee

from geetiles.config import SETTINGS

logging.basicConfig(
    level=SETTINGS.get("logging", {}).get("level"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y%m%d-%H:%M%p",
)


gee = SETTINGS.get("gee")
ee_user = gee.get("service_account")
private_key_file = gee.get("privatekey_file")
if private_key_file:
    logging.info(
        f"Initializing EE with privatekey.json credential file: {ee_user} | {private_key_file}"
    )
    credentials = ee.ServiceAccountCredentials(ee_user, private_key_file)
    ee.Initialize(credentials)
    ee.data.setDeadline(60000)
elif os.getenv("ENVIRONMENT") != "test":
    raise ValueError("privatekey.json file not found. Unable to authenticate EE.")

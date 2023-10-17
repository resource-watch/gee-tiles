"""The API MODULE"""

import os

import RWAPIMicroservicePython
from flask import Flask

from geetiles.config import SETTINGS
from geetiles.routes.api import error
from geetiles.routes.api.v1 import tile_endpoints


# Flask App
app = Flask(__name__)

# Routing
app.register_blueprint(tile_endpoints, url_prefix="/api/v1/layer")

# Integration with the RW API ecosystem
RWAPIMicroservicePython.register(
    app=app,
    gateway_url=os.getenv("GATEWAY_URL"),
    token=os.getenv("MICROSERVICE_TOKEN"),
    aws_cloud_watch_logging_enabled=(
        os.getenv("AWS_CLOUD_WATCH_LOGGING_ENABLED", "True").lower() == "true"
    ),
    aws_cloud_watch_log_stream_name=SETTINGS.get("service", {}).get("name"),
    aws_region=os.getenv("AWS_REGION"),
    require_api_key=(os.getenv("REQUIRE_API_KEY", "False").lower() == "true"),
)


@app.errorhandler(403)
def forbidden(e):
    return error(status=403, detail="Forbidden")


@app.errorhandler(404)
def page_not_found(e):
    return error(status=404, detail="Not Found (404)")


@app.errorhandler(405)
def method_not_allowed(e):
    return error(status=405, detail="Method Not Allowed")


@app.errorhandler(410)
def gone(e):
    return error(status=410, detail="Gone")


@app.errorhandler(500)
def internal_server_error(e):
    return error(status=500, detail="Internal Server Error")

#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.json
        echo -e "$GCLOUD_STORAGE" | base64 -d > storage.json
        exec python main.py
        ;;
    test)
        echo "Test"
        echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.json
        echo -e "$GCLOUD_STORAGE" | base64 -d > storage.json
        exec pytest
        ;;
    start)
        echo "Running Start"
        echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.json
        echo -e "$GCLOUD_STORAGE" | base64 -d > storage.json
        exec gunicorn -c gunicorn.py geetiles.app:app
        ;;
    *)
        exec "$@"
esac

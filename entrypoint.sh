#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.pem
        echo -e "$GCLOUD_STORAGE" | base64 -d > storage.json
        exec python main.py
        ;;
    test)
        echo "Test"
        
        ;;
    start)
        echo "Running Start"
        echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.pem
        echo -e "$GCLOUD_STORAGE" | base64 -d > storage.json
        exec gunicorn -c gunicorn.py ps:app
        ;;
    *)
        exec "$@"
esac

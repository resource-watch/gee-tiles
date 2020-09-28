# Gee tile server for microservices

[![Build Status](https://travis-ci.org/resource-watch/gee-tiles.svg?branch=dev)](https://travis-ci.org/resource-watch/gee-tiles)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6c8dd3205ab1cb4a0073/test_coverage)](https://codeclimate.com/github/resource-watch/gee-tiles/test_coverage)

## Dependencies

Dependencies on other Microservices:
- [Layer](https://github.com/resource-watch/layer)

## Getting started

### Requirements

You need to install Docker in your machine if you haven't already [Docker](https://www.docker.com/)

### Development

Follow the next steps to set up the development environment in your machine.

1. Clone the repo and go to the folder

```ssh
git clone https://github.com/resource-watch/gee-tiles
cd python-skeleton
```

2. Run the geetiles.sh shell script in development mode.

```ssh
./geetiles.sh develop
```

If this is the first time you run it, it may take a few minutes.

### Code structure

The API has been packed in a Python module (ps). It creates and exposes a WSGI application. The core functionality
has been divided in three different layers or submodules (Routes, Services and Models).

There are also some generic submodules that manage the request validations, HTTP errors and the background tasks manager.


### Tests

As this microservice relies on Google Earth Engine, tests require a valid `storage.json` or equivalent file. 
At the time of this writing, actual tests use mock calls, so the real credential are only needed because Google's 
library actually validates the credentials on startup. 

Before you run the tests, be sure to install the necessary development libraries, using `pip install -r requirements_dev.txt`.

Actual test execution is done by running the `pytest` executable on the root of the project.  

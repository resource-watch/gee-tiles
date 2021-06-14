## 14/06/2021

- Update `RWAPIMicroservicePython` to remove CT support.

## 02/06/2021

- Fix issue with `Werkzeug` version differences causing redirecting issues when loading from Redis cache.  

## 31/05/2021

- Update `RWAPIMicroservicePython` to add CORS support.

## 06/03/2021

- Update `RWAPIMicroservicePython` to fix issue with requests to other microservices.
- Fix issue when loading google metadata on startup.

## 12/02/2021

- Remove dependency on CT's `authenticated` functionality

## 22/01/2021

- Replace CT integration library

# 1.1.0

## 17/11/2020

- `expire-cache` endpoint is now only accessible by microservices
- Remove filter dependency for `expire-cache` endpoint
- Remove MapId caching on Redis
- Update GEE integration library to 0.1.236, update other dependencies
- Improved logging 


# 1.0.0

## 09/04/2020

- Add node affinity to kubernetes configuration.

## 19/03/2020

- Update `Flask`, `urllib3` and `requests` packages.

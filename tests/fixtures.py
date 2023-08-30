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
        "name": 'John Manager',
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
        "name": 'John User',
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
    "MICROSERVICE": {
        "id": 'microservice'
    },
}

TML_LAYER = {
   "data":{
      "id":"e8f9a96a-0a2c-4cf9-b904-36531f23a8b2",
      "type":"layer",
      "attributes":{
         "name":"TML_sld_layer",
         "slug":"TML_sld_layer",
         "dataset":"e9e91ed6-22b0-4280-8710-34589b0b1336",
         "description":"",
         "application":[
            "rw"
         ],
         "iso":[
            
         ],
         "provider":"gee",
         "userId":"58fde4354eecd9073107af0f",
         "default":True,
         "protected":False,
         "published":True,
         "env":"preproduction",
         "layerConfig":{
            "body":{
               "sldValue":"<RasterSymbolizer><ColorMap extended=\"false\" type=\"intervals\"><ColorMapEntry color=\"#ebf5eb\" quantity=\"0\" label=\"0-20\" opacity=\"0\"/><ColorMapEntry color=\"#ebf5eb\" quantity=\"20\" label=\"0-20\"/><ColorMapEntry color=\"#a0d796\" quantity=\"30\" label=\"20-40\"/><ColorMapEntry color=\"#68b869\" quantity=\"40\" label=\"20-40\"/><ColorMapEntry color=\"#68b869\" quantity=\"50\" label=\"40-60\"/><ColorMapEntry color=\"#2c8e4a\" quantity=\"60\" label=\"40-60\"/><ColorMapEntry color=\"#2c8e4a\" quantity=\"70\" label=\"60-80\"/><ColorMapEntry color=\"#0f803a\" quantity=\"80\" label=\"80-100\"/><ColorMapEntry color=\"#0f803a\" quantity=\"90\" label=\"80-100\"/><ColorMapEntry color=\"#0f803a\" quantity=\"100\" label=\"80-100\"/><ColorMapEntry color=\"#000000\" quantity=\"255\" label=\"255\" opacity=\"0\"/></ColorMap></RasterSymbolizer>",
               "styleType":"sld"
            },
            "assetId":"projects/wri-datalab/TML",
            "isImageCollection":True,
            "provider":"gee",
            "position":"mosaic"
         },
         "legendConfig":{
            "type":"choropleth",
            "items":[
               {
                  "name":"0-20",
                  "color":"#edf8e9",
                  "id":0
               },
               {
                  "name":"20-40",
                  "color":"#a0d796",
                  "id":1
               },
               {
                  "name":"40-60",
                  "color":"#68b869",
                  "id":2
               },
               {
                  "name":"60-80",
                  "color":"#2c8e49",
                  "id":3
               },
               {
                  "name":"80-100",
                  "color":"#076f2f",
                  "id":4
               }
            ]
         },
         "interactionConfig":{
            
         },
         "applicationConfig":{
            
         },
         "staticImageConfig":{
            
         },
         "createdAt":"2021-10-14T13:42:22.034Z",
         "updatedAt":"2021-10-14T13:42:22.034Z"
      }
   }
}

AC_LAYER = {
    "data": {
        "id": "d787d894-f7af-47c4-af0f-0849b06686ee",
        "type": "layer",
        "attributes": {
            "name": "2015 Accessibility to Cities",
            "slug": "Travel-Time-to-Major-Cities_1",
            "dataset": "ccbcaf7b-1619-4298-8275-b135d1e8e04e",
            "description": "Time it takes to travel to the nearest city in 2015. Units are minutes, hours, days, and months.",
            "application": [
                "rw"
            ],
            "iso": [],
            "provider": "gee",
            "userId": "5980838ae24e6a1dae3dd446",
            "default": True,
            "protected": False,
            "published": True,
            "env": "production",
            "layerConfig": {
                "body": {
                    "sldValue": "<RasterSymbolizer>    <ColorMap  type=\"ramp\" extended=\"false\" >      '<ColorMapEntry color=\"#FFFFFF\" quantity=\"0\" opacity=\"1\" />' +    '<ColorMapEntry color=\"#C0F09C\" quantity=\"60\" opacity=\"1\" />' +    '<ColorMapEntry color=\"#E3DA64\" quantity=\"120\"  />' +  '<ColorMapEntry color=\"#D16638\" quantity=\"180\"  />' +    '<ColorMapEntry color=\"#BA2D2F\" quantity=\"360\" />' +   '<ColorMapEntry color=\"#A11F4A\" quantity=\"720\"  />' +    '<ColorMapEntry color=\"#730D6F\" quantity=\"1440\"  />' +    '<ColorMapEntry color=\"#0D0437\" quantity=\"20160\"  />' +  '<ColorMapEntry color=\"#00030F\" quantity=\"41556\"  />' +    </ColorMap></RasterSymbolizer>",
                    "styleType": "sld",
                    "url": "https://staging-api.globalforestwatch.org/v1/layer/d787d894-f7af-47c4-af0f-0849b06686ee/tile/gee/{z}/{x}/{y}"
                },
                "assetId": "Oxford/MAP/accessibility_to_cities_2015_v1_0",
                "type": "gee"
            },
            "legendConfig": {
                "items": [
                    {
                        "name": "0 h",
                        "color": "#FFFFFF"
                    },
                    {
                        "color": "#C0F09C",
                        "name": "1 h"
                    },
                    {
                        "color": "#E3DA64",
                        "name": "2 h"
                    },
                    {
                        "color": "#D16638",
                        "name": "3 h"
                    },
                    {
                        "color": "#BA2D2F",
                        "name": "6 h"
                    },
                    {
                        "color": "#A11F4A",
                        "name": "12 h"
                    },
                    {
                        "color": "#730D6F",

                        "name": "1 d"
                    },
                    {
                        "color": "#0D0437",
                        "name": "14 d"
                    },
                    {
                        "color": "#00030F",
                        "name": "1 m"
                    }
                ],
                "type": "choropleth"
            },
            "interactionConfig": {},
            "applicationConfig": {},
            "staticImageConfig": {},
            "createdAt": "2020-02-12T11:19:24.568Z",
            "updatedAt": "2020-02-12T12:18:00.198Z"
        }
    }
}

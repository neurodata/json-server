import requests


payload = {
    "payload": {
        "layers": {
            "Anti_5HT_MeanOf40": {
                "source": "boss://https://api.boss.neurodata.io/ZBrain/ZBrain/Anti_5HT_MeanOf40?window=0,50033",
                "type": "image",
                "opacity": 1,
                "blend": "additive",
                "color": "#281bd1",
                "max": 0.22
            },
            "ZBB_ath5-GFP": {
                "source": "boss://https://api.boss.neurodata.io/ZBrain/ZBrain/ZBB_ath5-GFP?window=0,7688",
                "type": "image",
                "opacity": 1,
                "blend": "additive",
                "color": "#3cb44b",
                "max": 0.92
            },
            "ZBB_y300-Gal4": {
                "source": "boss://https://api.boss.neurodata.io/ZBrain/ZBrain/ZBB_y300-Gal4",
                "type": "image",
                "opacity": 1,
                "blend": "additive",
                "color": "#ff0000",
                "max": 0.21
            },
            "zbrain_atlas": {
                "source": "precomputed://https://s3.amazonaws.com/zbrain/atlas_owen",
                "type": "segmentation",
                "selectedAlpha": 0.24,
                "objectAlpha": 0.55,
                "segments": [
                    "1",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "2",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "3",
                    "30",
                    "31",
                    "32",
                    "33",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9"
                ]
            }
        },
        "navigation": {
            "pose": {
                "position": {
                    "voxelSize": [
                        798,
                        798,
                        2000
                    ],
                    "voxelCoordinates": [
                        585.0491943359375,
                        261.55596923828125,
                        13
                    ]
                }
            },
            "zoomFactor": 1638.3988682407064
        },
        "perspectiveOrientation": [
            0.6896195411682129,
            -0.15406320989131927,
            0.10602857917547226,
            -0.6996051073074341
        ],
        "perspectiveZoom": 8557.5200670284,
        "jsonStateServer": "https://api.myjson.com/bins",
        "selectedLayer": {
            "layer": "zbrain_atlas"
        },
        "layout": "4panel"
    }
}

url = 'https://json.neurodata.io/bins/default/NGState-microservice'
headers = {'Content-type': 'application/json'}
r = requests.post(url, json=payload)
print(r.json())


url = 'https://json.neurodata.io/bins/default/NGState-microservice?NGStateID=b8rw7q2DrhUOiw'
headers = {'Content-type': 'application/json'}
r = requests.get(url, headers=headers)
print(r.json())

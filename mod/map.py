import os

MapSetting = {
    "600x400": {
        "type": "600x400",
        "worldX": 1202,
        "worldY": 400,
        "unit": 20,
        "ball": 14,
        "end-font": 40
    },
    "900x600": {
        "type": "900x600",
        "worldX": 1802,
        "worldY": 600,
        "unit": 30,
        "ball": 20,
        "end-font": 80
    }
}

currentMap = MapSetting['900x600']
# currentMap = MapSetting['600x400']

image_path = os.path.join(os.getcwd(), "images")
font_path = os.path.join(os.getcwd(), "fonts")
sound_path = os.path.join(os.getcwd(), "music")
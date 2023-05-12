import json


def get(attr):
    with open('config.json', 'r') as f:
        config = json.load(f)
        if attr in config.keys():
            return config[attr]

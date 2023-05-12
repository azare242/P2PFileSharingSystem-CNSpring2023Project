import json

def get(_type):
    with open('url.json', 'r') as f:
        url = json.load(f)
        if _type in url.keys():
            return url[_type]
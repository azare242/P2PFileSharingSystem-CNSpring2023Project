import requests


class HTTPConnection:
    def __init__(self):
        self.get = requests.get
        self.post = requests.post

import json
import socket
import os


class Config:
    __instance = None

    @staticmethod
    def get_instance():
        if not Config.__instance:
            Config()
        return Config.__instance

    def __init__(self):
        self.config = None
        if Config.__instance:
            raise Exception("Config class is a Singleton. Use get_instance() method to get the instance.")
        else:
            Config.__instance = self
            self.load_config()

    def load_config(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_directory, 'config.json')
        with open(config_path, 'r') as f:
            self.config = json.load(f)



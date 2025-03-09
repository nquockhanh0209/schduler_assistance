import os
from threading import Lock



# log_config = LogConfig(__name__)
# logger = log_config.logger


class ConfigMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=ConfigMeta):
    
    def __init__(self):
        if "BOT_TOKEN" in os.environ:
            self.BOT_TOKEN = os.environ["BOT_TOKEN"]
        if "MONGODB_HOST" in os.environ:
            self.MONGODB_HOST = os.environ["MONGODB_HOST"]
        if "DB_NAME" in os.environ:
            self.DB_NAME = os.environ["DB_NAME"]
       

    
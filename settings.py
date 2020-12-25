from os import urandom

class BaseConfig():
    DEBUG = True
    SERVER_NAME = 'localhost:80'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SERVER_NAME = '0.0.0.0:443'
    SECRET_KEY = urandom(512)


class DevelopmentConfig(BaseConfig):
    SERVER_NAME = 'localhost:443'
    USE_RELOADER = True
    TESTING = True
    SECRET_KEY  = b'ababababa'
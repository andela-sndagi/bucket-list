class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'bucketlist_app.db'


class TestingConfig(Config):
    TESTING = True


config = {
    "development": "DevelopmentConfig",
    "testing": "TestingConfig",
    "default": "DevelopmentConfig"
}

class Config(object):
    """Default Settings"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """setting Testing configuration"""
    DEBUG = True


class TestingConfig(Config):
    """setting Testing configuration"""
    TESTING = True


CONFIG = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}

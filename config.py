import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DATABASE = '/tmp/flaskr.db'
    DEBUG = True
    SECRET_KEY = 'development'
    USERNAME = 'admin'
    PASSWORD = 'lsof04Mt'

    @staticmethod 
    def init_app(app):
        pass

class TestingConfig(Config):
    TESTING = True SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \ 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \ 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {

'development': DevelopmentConfig, 'testing': TestingConfig, 'production': ProductionConfig,

'default': DevelopmentConfig

}
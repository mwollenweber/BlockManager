'''
Copyright Matthew Wollenweber 2014


'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://blockmanager:bmanager@localhost/BlockManager'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.gwu.edu'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://blockmanager:bmanager@localhost/BlockManager'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://blockmanager:bmanager@localhost/BlockManager'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        
        credentials = None
        secure = None
        #if getattr(cls, 'MAIL_USERNAME', None) is not None:
            #credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            #if getattr(cls, 'MAIL_USE_TLS', None):
                #secure = ()
        #mail_handler = SMTPHandler(
            #mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            #fromaddr=cls.FLASKY_MAIL_SENDER,
            #toaddrs=[cls.FLASKY_ADMIN],
            #subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            #credentials=credentials,
            #secure=secure)
        #mail_handler.setLevel(logging.ERROR)
        #app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

from os import environ, path
from dotenv import load_dotenv

# basedir = path.abspath(path.dirname(__name__))
# load_dotenv(path.join(basedir, '.env'))
load_dotenv('.env')


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = environ.get('SECRET_KEY')
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    # mail configure
    MAIL_PORT = 465
    MAIL_DEBUG = False
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_SERVER = ''
    MAIL_USERNAME = ''
    MAIL_DEFAULT_SENDER = ''
    MAIL_PASSWORD = ''

    # redis configure
    REDIS_URI = environ.get('REDIS_URI')
    QUEUES = environ.get('QUEUES')


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    MAIL_DEBUG = True

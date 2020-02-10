import os


class Config:
    # Database Server and config
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')

    DB_USER = os.getenv('DB_USER', 'spicylola')
    DB_PASS = os.getenv('DB_PASS', 'ohsospicy')
    DB_DATABASE = os.getenv('DB_DATABASE', 'gql_example')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?'


class LocalConfig(Config):
    '''Local configuration.'''

    ENV = 'local'
    DEBUG = True
    LOGLEVEL = 'DEBUG'

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


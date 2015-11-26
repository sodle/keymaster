import psycopg2
from os import environ

# Base URL of the web server
BASE_URL = environ.get('KM_BASE_URL')
# Base URL for shortlinks (if enabled)
BASE_SHORTENER_URL = environ.get('KM_BASE_SHORT_URL')


# Return a connection to the Postgresql database
def DB_CONNECTION():
    db = environ.get('KM_POSTGRES_DB')
    user = environ.get('KM_POSTGRES_USER')
    return psycopg2.connect(database=db, user=user)


# Random salt to use for hashids
HASH_SALT = environ.get('KM_HASHIDS_SALT')


# Where to store logs, how often to rotate them, and how many to keep
LOGGING_LOCATION = environ.get('KM_LOG_LOCATION')
LOGGING_FREQUENCY = environ.get('KM_LOG_FREQUENCY')
LOGGING_RETENTION = int(environ.get('KM_LOG_RETENTION'))


# Connections to services where keys can be installed.
SERVICE_CONNECTORS = {}

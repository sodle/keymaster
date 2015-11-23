import psycopg2

# Base URL of the web server
BASE_URL = 'http://keymaster.com'

# Base URL for shortlinks (if enabled)
BASE_SHORTENER_URL = 'http://key.io'


# Return a connection to the Postgresql database
def DB_CONNECTION():
    return psycopg2.connect(database='keymaster', user='zuul')

# Random salt to use for hashids
HASH_SALT = 'stay_puft'

# Where to store logs, how often to rotate them, and how many to keep
LOGGING_LOCATION = '/var/log/keymaster/keymaster.log'
LOGGING_FREQUENCY = 'midnight'
LOGGING_RETENTION = 10

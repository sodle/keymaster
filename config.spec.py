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

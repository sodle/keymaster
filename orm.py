import config
from hashids import Hashids
import urlparse

# ID Hasher
hasher = Hashids(salt=config.HASH_SALT)

# Push an ID to the database and get the hashid for it.
def upload_key(public_key):
    conn = config.DB_CONNECTION()
    cur = conn.cursor()
    insert_query = ("INSERT INTO uploaded_key (public_key) "
                    "VALUES (%s) RETURNING upload_id")
    cur.execute(insert_query, [public_key])
    db_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return hasher.encode(db_id)

# Get a key back from the database by its hashid.
def fetch_key(hashid):
    conn = config.DB_CONNECTION()
    cur = conn.cursor()
    db_id = hasher.decode(hashid)
    select_query = ("SELECT * FROM uploaded_key WHERE upload_id=%s "
                    "AND expire_time>current_timestamp")
    cur.execute(select_query, [db_id])
    key_obj = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return key_obj

# Force a key to expire.
def expire_key(hashid):
    conn = config.DB_CONNECTION()
    cur = conn.cursor()
    db_id = hasher.decode(hashid)
    update_query = ("UPDATE uploaded_key SET expire_time=current_timestamp "
                    "WHERE upload_id=%s")
    cur.execute(update_query, [db_id])
    conn.commit()
    cur.close()
    conn.close()

# Extend a key's expiration by 30 minutes.
def extend_key(hashid):
    conn = config.DB_CONNECTION()
    cur = conn.cursor()
    db_id = hasher.decode(hashid)
    update_query = ("UPDATE uploaded_key "
                    "SET expire_time=expire_time+interval '30 minutes' "
                    "WHERE upload_id=%s AND expire_time>current_timestamp")
    cur.execute(update_query, [db_id])
    conn.commit()
    cur.close()
    conn.close()

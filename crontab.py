import config
import psycopg2
import schedule
import threading
import time
import keymaster


def prune_db():
    keymaster.logger.info('Pruning expired keys from database.')
    conn = config.DB_CONNECTION()
    cur = conn.cursor()
    update_query = ("UPDATE uploaded_key SET public_key='' "
                    "WHERE expire_time<current_timestamp"
                    )
    cur.execute(update_query)
    conn.commit()
    cur.close()
    conn.close()

schedule.every(60).minutes.do(prune_db)

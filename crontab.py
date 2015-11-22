import config
import psycopg2
import schedule
import threading
import time

def prune_db():
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

class Crontab(threading.Thread):
    @classmethod
    def run(cls):
        schedule.run_all()
        while True:
            schedule.run_pending()
            time.sleep(600)
tab = Crontab()
tab.start()

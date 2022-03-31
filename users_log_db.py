import sqlite3
import datetime

DB_PATH = 'db/users_log.db'

def add_log_record(event_data):
    user_id = event_data['user_id']
    user_name = event_data['user_name']
    event = event_data['event']
    session_time = datetime.datetime.now()

    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS users_sessions ('
                       'id INTEGER PRIMARY KEY,'
                       'user_id INTEGER NOT NULL,'
                       'user_name TEXT,'
                       'event TEXT,'
                       'session_time TEXT)')

        cursor.execute('INSERT INTO users_sessions (user_id, user_name, event, session_time) VALUES (?,?,?,?)', (user_id, user_name, event, session_time))

        db_connection.commit()


# Запрос количества пользователей за период
def get_users_count(start_date, end_date):
    users_count = 0

    with sqlite3.connect(DB_PATH) as db_connection:
        cursor = db_connection.cursor()
        cursor.execute(f'SELECT DISTINCT user_id FROM users_sessions WHERE session_time BETWEEN "{start_date} 00:00:00" AND "{end_date} 23:59:59"')
        users_count = len(cursor.fetchall())

    return users_count            
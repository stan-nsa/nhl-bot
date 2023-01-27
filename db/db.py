import sqlite3

DB_PATH = 'db/hdd-nsa-bot.sqlite'

db_conn = None
db_cur = None

def db_connect():

    global db_conn, db_cur

    try:
        db_conn = sqlite3.connect(DB_PATH)
        db_cur = db_conn.cursor()
        print("Подключение к sqlite выполнено")

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


def db_close():
    global db_conn, db_cur

    if (db_conn):
        db_cur.close()
        db_conn.close()
        print("База sqlite закрыта")


def insert_user(user):
    global db_conn, db_cur

    db_connect()

    try:
        params = (user['id'], user['username'], user['first_name'], user['last_name'])
        q = 'REPLACE INTO users(id, username, first_name, last_name) VALUES(?, ?, ?, ?)'

        db_cur.execute(q, params)
        db_conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    db_close()


def insert_favorites(user, team : str, type='favorites'):
    global db_conn, db_cur

    insert_user(user)

    db_connect()

    team = team.split(':')

    try:
        params = (user['id'], type, team[0], team[1])
        q = 'REPLACE INTO user_teams(user_id, type, team_id, team_name) VALUES(?, ?, ?, ?)'

        db_cur.execute(q, params)
        db_conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    db_close()


def get_user_favorites_teams(user, type='favorites'):
    global db_conn, db_cur
    user_teams = None

    db_connect()

    try:
        params = (user['id'], type)
        q = 'SELECT team_id FROM user_teams WHERE user_id = ? AND type = ?'

        db_cur.execute(q, params)

        user_teams = db_cur.fetchall()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    db_close()

    return user_teams



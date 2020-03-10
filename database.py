import sqlite3
from user import User

conn = None
cur  = None
cur_user = None

def connect(path):
    global conn, cur
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(' PRAGMA foreign_keys=ON; ')
    conn.commit()

def set_user(email, name, city, gender):
    global cur_user
    cur_user = User(email, name, city, gender)
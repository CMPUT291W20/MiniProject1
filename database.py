import sqlite3
from user import User

conn     = None  # Connection to database
cur      = None  # Cursor for database
cur_user = None  # Currently logged in user data

def connect(path):
    # Connect the database to the passed in path

    global conn, cur
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(' PRAGMA foreign_keys=ON; ')
    conn.commit()

def set_user(email, name, city, gender):
    # The current user with passed in email, name, city, gender
    global cur_user
    cur_user = User(email, name, city, gender)
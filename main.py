import os, sys
import sqlite3
from external_func import clear_screen, close_program
import database as db
from users import user_search
from user import User
from datetime import datetime
from startup import start
import random, string, re

user = None

def main():
    filename = sys.argv[-1]  # Get the last agument passed to the file name
    if filename == "main.py":
        print("Error: No database passed to file")
        print("Exiting program...")
        sys.exit()
    path = "./" + filename
    db.connect(path)

    isQuit = False
    while not isQuit:
        start()
        mainMenu()
        clear_screen()
        db.cur_user = None  # User has logged out, set user to none


def mainMenu():
    logout = False
    while not logout:
        clear_screen()
        print("Welcome to MiniProject 1 Store Main Menu")
        print("1. List products  2. Search for sales  3. Post a sale  4. Search for users  Logout: Logout of account  Exit: Exit Program")
        select = input("Select: ")
        if select == "logout":
            logout = True
        elif select.lower() == "exit":
            close_program()
        elif select == "1":
            pass
        elif select == "2":
            pass
        elif select == "3":
            post_sale()
        elif select == "4":
            user_search()
        else:
            print("Invalid selection made")


def post_sale():
    clear_screen()
    print("Please enter the following information to post a sale:")
    pid = input("Product ID (Optional, press Enter to skip): ")
    if pid == "":
        pid = None

    edate = get_datetime()

    valid_input = False
    while not valid_input:
        desc = input("Sale Description (Max 25 char): ")
        if len(desc) <= 25:
            valid_input = True
        else:
            print("Error: input length to long")

    valid_input = False
    while not valid_input:
        cond = input("Condition (max 10 char): ")
        if len(cond) <= 10:
            valid_input = True
        else:
            print("Error: input length to long")

    r_price = input("Reserved price (Optional, press Enter to skip): ")
    if r_price == "":
        r_price = None

    sid = generateSID()
    db.cur.execute("INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)", (sid, user.get_email(), edate, desc, cond, r_price))

def get_datetime():
    # Promps the user to enter a correct date and time format for a sales end date and time
    now = datetime.now()
    now_datetime = now.strftime("%Y-%m-%d %H:%M")

    valid_input = False
    while not valid_input:
        date = input("End date in format yyyy-mm-dd ")
        if len(date) == 10:
            pass
        else:
            print("Error: Invalid format")
    
    time = input("End time in format HH:MM ")
    edate = date + " " + time
    return edate


def generateSID():
    # Generate a random sale id (sid) that does not exist yet
    char = string.ascii_letters + "0123456789"

    valid_sid =  False
    while not valid_sid:
        sid = ''.join(random.choice(char) for i in range(4))
        db.cur.execute("SELECT sid FROM sales WHERE sid=?", (sid,))
        data = db.cur.fetchall()
        if not data:
            # The sid is avaiable for use
            valid_sid =  True
    return sid

main()
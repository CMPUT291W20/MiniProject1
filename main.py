import os, sys
import sqlite3
from database import *
from user import User

conn = None  # Connection
cur  = None  # Cursor
user = None  # The logged in user

def main():
    global conn, cur, user
    path = "./mp1.db"
    conn, cur = connect(path)
    drop_tables(cur)
    define_tables(conn,cur)

    isQuit = False
    while not isQuit:
        user = start()
        mainMenu(user)
        clear_screen()
        user = None  # User has logged out, set user to none


def start():
    # Prompts user to select login, register, or exit program
    # return:
    #   user: upon successful login or register
    #   -2: upon selection of quit
    valid_entry = False

    while not valid_entry:
        print("Welcome to the MiniProject 1 Store")
        print("1: Login  2. Register  Exit: Exit application")
        select = input("Slection: ")

        if (select == '1'):
            user = login()
            if user != -1:
                valid_entry = True
        if (select == '2'):
            user = register()
            if user != -1:
                valid_entry = True
        if (select.lower() == 'exit'):
            close_program()
        else:
            clear_screen()
            print("Invalid entry")
    return user


def login():
    # Gets the email and password of an existing user
    # return:
    #   user: if the email and password exists
    #   -1: if the user selects to go back
    global conn, cur
    clear_screen()

    valid_login = False
    while not valid_login:
        print("Enter email and password. Type 'back' to go back")
        email = input("Email: ")
        if (email.lower() == 'back'):
            email = -1
            break
        pwd = input("Password: ")

        user_data = getUser(email)
        print(user_data)
        if user_data:
            # There is data in the tuple
            if pwd == user_data[2]:
                email = user_data[0]
                valid_login = True
            else:
                clear_screen()
                print("Invalid email/password")
        else:
            # There is no data in the tuple
            clear_screen()
            print("Invalid email/password")   
    return email


def register():
    # Gets the information of the user to register for the database
    # return:
    #   user: if data provided is valid
    #   -1: if the user selects to go back
    global conn, cur
    valid_entry = False
    clear_screen()
    print("Register for new account")

    while not valid_entry:
        email = input("Email: ")
        user_data = getUser(email)
        if user_data:
            print("Email already in use")
        else:
            valid_entry = True
    name = input("Name: ")
    pwd = input("Password: ")
    city = input("City: ")

    valid_entry = False
    while not valid_entry:
        gender = input("Gender (M/F): ")
        if gender == "M" or gender == "F":
            valid_entry = True
        else:
            print("Entry is invalid, Please enter M or F for gender")

    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (email, name, pwd, city, gender))
    conn.commit()
    new_user = User(email, name, city, gender)
    return new_user


def getUser(email):
    # Takes in a string email address, and finds the users data in the database with that email
    # return: Truple of the users data: (email, name, pwd, city, gender)
    global conn, cur
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user_data = cur.fetchone()
    return user_data


def mainMenu(user):
    clear_screen()
    print("Welcome to MiniProject 1 Store Main Menu")
    print("1. List products  2. Search for sales  3. Post a sale  4. Search for users  Logout: Logout of account  Exit: Exit Program")
    logout = False
    while not logout:
        select = input("Select: ")
        if select.lower() == "logout":
            logout = True
        elif select.lower() == "exit":
            close_program()
        elif select == "1":
            pass
        elif select == "2":
            pass
        elif select == "3":
            pass
        elif select == "4":
            pass
            #user_search()
        else:
            print("Invalid selection made")
 

def clear_screen():
    if sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("clear")

def close_program():
    clear_screen()
    print("Thank you for shopping with us")
    print("Exiting Program....")
    sys.exit()

main()
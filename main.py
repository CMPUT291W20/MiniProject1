import os, sys
import sqlite3
from database import *

conn = None  # Connection
cur  = None  # Cursor

def main():
    global conn, cur
    path = "./mp1.db"
    conn, cur = connect(path)
    drop_tables(cur)
    define_tables(conn,cur)

    isQuit = False
    while not isQuit:
        user = start()
        if user == -2:
            isQuit = True
        mainMenu(user)

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
            user = -2
            valid_entry = True
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
    valid_login = False

    while not valid_login:
        clear_screen()
        print("Enter email and password. Type 'back' to go back")
        email = input("Email: ")
        if (email.lower() == 'back'):
            email = -1
            break
        pwd = input("Password: ")

        user_data = getUser(email)
        if user_data:
            # There is data in the tuple
            if pwd == user_data[1]:
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

    cur.execute("INSERT INTO users(email, name, pwd, city, gender) VALUES email=:e, name=:n, pwd=:p, city=:c, gender=:g;", 
                {"e":email, "n":name, "p":pwd, "c":city, "g":gender})
    conn.commit()
    return user_data[0]

def getUser(email):
    # Takes in a string email address, and finds the users data in the database with that email
    # return: Truple of the users data: (email, name, pwd, city, gender)
    global conn, cur
    cur.execute("SELECT * FROM users WHERE email=:e", {"e":email})
    user_data = cur.fetchone()
    return user_data

def print_reviews(email):
    global cur
    # Takes in the email whom's reviews are to be printed

    cur.execute("SELECT * FROM reviews WHERE email:e", {"e":email})
    list = cur.fetchall()

    if list:
        # There are tuples in the list
        dash = '-' * 90
        print(dash)
        print('{:<22s} {:<22s} {:<8s} {:<22s} {:<10s}'.format("Reviewer", "Reviewee", "Rating", "Description", "Date"))
        print(dash)
        for tuple in list:
            print('{:<22s} {:<22s} {:<8f} {:<22s} {:<10s}'.format(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]))
    else:
        # There are no tuples in the list
        print("This user has no reviews")


def mainMenu(user):
    clear_screen()
    

def clear_screen():
    if sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("clear")


main()
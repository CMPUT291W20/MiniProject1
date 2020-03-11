import sqlite3
from external_func import clear_screen, close_program
import database as db
from user import User

def start():
    # Prompts user to select login, register, or exit program
    # return:
    #   user: upon successful login or register
    #   -2: upon selection of quit

    clear_screen()
    
    valid_entry = False
    while not valid_entry:
        print("Welcome to the MiniProject 1 Store")
        print("1: Login  2. Register  3: Exit application")
        select = input("Selection: ")
        print(type(select))
        print(select)
        
        if (select == "1"):
            user = login()
            if user != -1:
                valid_entry = True
        if (select == "2"):
            user = register()
            if user != -1:
                valid_entry = True
        if (select == "3"):
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
    clear_screen()

    valid_login = False
    while not valid_login:
        print("Enter email and password. Type 'back' to go back")
        email = input("Email: ")
        if (email.lower() == 'back'):
            login_user = -1
            break
        pwd = input("Password: ")

        user_data = getUser(email)
        print(user_data)
        if user_data:
            # There is data in the tuple
            if pwd == user_data[2]:
                login_user = User(user_data[0], user_data[1], user_data[3], user_data[4])
                db.cur_user = login_user
                valid_login = True
            else:
                clear_screen()
                print("Invalid email/password")
        else:
            # There is no data in the tuple
            clear_screen()
            print("Invalid email/password")   
    return login_user

def register():
    # Gets the information of the user to register for the database
    # return:
    #   user: if data provided is valid
    #   -1: if the user selects to go back
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

    db.cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (email, name, pwd, city, gender))
    db.conn.commit()
    db.set_user(email, name, city, gender)
    return db.cur_user


def getUser(email):
    # Takes in a string email address, and finds the users data in the database with that email
    # return: Truple of the users data: (email, name, pwd, city, gender)
    db.cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user_data = db.cur.fetchone()
    return user_data
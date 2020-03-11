import os, sys
import sqlite3
from external_func import clear_screen, close_program
import database as db
from products import list_products
from users import user_search
from user import User
from startup import start
from sales import post_sale, sale_search

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
    # Main menu of the program that prompts the user with the first initial options to choose from
    
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
            list_products()
        elif select == "2":
            sale_search()
        elif select == "3":
            post_sale()
        elif select == "4":
            user_search()
        else:
            print("Invalid selection made")

main()
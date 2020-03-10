import os, sys
import sqlite3

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
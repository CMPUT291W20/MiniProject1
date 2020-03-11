import os, sys
import database as db
import random
from datetime import datetime

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

def place_bid(sID_choice, maxAmt):
    print("Placing a bid for {}:".format(sID_choice))

    amount = int(input("Enter a bid amount: "))
    if amount <= maxAmt:
        print("Bid is not larger then the current highest price")
    else:
        valid_bid = False
        while not valid_bid:
            bID = random.randint(1,999999999)
            db.cur.execute("select * from bids where bid = ?", (str(bID),))
            returned = db.cur.fetchone()
            if not returned:
                valid_bid = True

        bidder = db.cur_user.get_email()
        now = datetime.now()
        bdate = now.strftime("%Y-%m-%d %H:%M")

        data = (bID, bidder, sID_choice, bdate, amount)
        db.cur.execute("INSERT INTO bids VALUES (?, ?, ?, ?, ?)", data)
        db.conn.commit()
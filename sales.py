# Need to figure out imports and how to get files to work together properly
import sqlite3, random, string, re
import database as db
from external_func import clear_screen, place_bid, get_sale_select, print_active_sale
from datetime import datetime, date
from users import print_reviews, user_active_sales
from user import User

def sale_select(sID_choice):
    # From functionality 3 in spec 
    row = get_sale_select(sID_choice)

    print("""
            What would you like to do with this selection?
            1. Place bid on the selected sale
            2. List all active sales by seller
            3. List reviewes of the seller
            """)
    valid_input =  False
    while not valid_input:
        action = input("Select an action (1, 2, or 3): ")
        valid_input = True
        if action == "1":
            place_bid(sID_choice, row[6])
        elif action == "2":
            user_active_sales(row[0])
        elif action == "3":
            print_reviews(row[0])
        else: 
            valid_input = False
            print("Invalid selection.") 


def active_sales(pID_choice):
    # List all active sales associated to the product, ordered based on the remaining time of the sale; includes the sale description, the maximum bid (if there is a bid on the item) or the reserved price (if there is no bid on the item), and the number of days, hours and minutes left until the sale expires
    clear_screen()
    sale_listing = """
                    select s.sid, s.descr, CASE WHEN maxAmt IS NULL THEN (CASE WHEN s.rprice IS NULL THEN 0 ELSE s.rprice END) ELSE maxAmt END, s.edate, datetime('now')
                    from sales s left join 
                    (select sid, max(amount) as maxAmt from bids group by sid) b on b.sid = s.sid
                    where pid = "{pid}"
                    and s.edate > datetime('now')
                    """
    sale_query = sale_listing.format(pid=pID_choice)
    db.cur.execute(sale_query)
    rows = db.cur.fetchall()

    index = print_active_sale(rows)
    sale_select(rows[index][0])

def sale_search():
    # Prompts user to enter keywords to use to compare to descriptions in query
    # Prints out the results
    search = input("Enter keywords to search for active sales: ")
    search_input = "%" + search + "%"
    search_listing = """
                select distinct s.sid, s.descr, CASE WHEN maxAmt IS NULL THEN (CASE WHEN s.rprice IS NULL THEN 0 ELSE s.rprice END) ELSE maxAmt END, s.edate, datetime('now')
                from sales s left join 
                (select sid, max(amount) as maxAmt from bids group by sid) b on b.sid = s.sid left join products p on p.pid = s.pid
                where s.descr like "{search_1}" or p.descr like "{search_2}"
                and s.edate > datetime('now')
                """

    search_query = search_listing.format(search_1=search_input, search_2=search_input)
    db.cur.execute(search_query)
    rows = db.cur.fetchall()

    index = print_active_sale(rows)
    sale_select(rows[index][0])


def post_sale():
    clear_screen()

    print("Please enter the following information to post a sale:")
    valid_pid = False
    while not valid_pid:
        pid = input("Product ID (Optional, press Enter to skip): ")
        if pid == "":
            pid = None
            valid_pid = True
        else:
            db.cur.execute("SELECT * FROM products WHERE pid=?", (pid,))
            results = db.cur.fetchall()
            if results:
                valid_pid = True
            else:
                print("The pid: " + pid + " Does not exist")

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
    db.cur.execute("INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?)", (sid, db.cur_user.get_email(), pid, edate, desc, cond, r_price))
    db.conn.commit()

def get_datetime():
    # Promps the user to enter a correct date and time format for a sales end date and time
    now = datetime.now()
    now_datetime = now.strftime("%Y-%m-%d %H:%M")

    future_date = False
    while not future_date:
        valid_input = False
        while not valid_input:
            date = input("End date in format yyyy-mm-dd ")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                valid_input = True
            except:
                print("Incorrect date format")
        valid_input = False
        while not valid_input:
            time = input("End time in format HH:MM ")
            try:
                datetime.strptime(time, "%H:%M")
                valid_input = True
            except:
                print("Incorrect time format")
        edate = date + " " + time
        if edate > now_datetime:
            future_date = True
        else:
            print("date needs tp be in the future")
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
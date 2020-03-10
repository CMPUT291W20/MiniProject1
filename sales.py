# Need to figure out imports and how to get files to work together properly
import sqlite3, random, string, re
import database as db
from external_func import clear_screen
from datetime import datetime
from user import User

def place_bid(sID_choice):
    print("Placing a bid for {}:".format(sID_choice))

    bID = db.cur.execute("select count(*) from bids;")
    bidder = db.cur_user.get_email()
    bdate = datetime.now()
    amount = int(input("Enter a bid amount: "))

    data = (bID, bidder, sID_choice, bdate, amount)
    db.cur.execute("insert into bids (?, ?, ?, ?, ?);", data)
    db.cur.commit()

def sale_select():
    # From functionality 3 in spec 
    sID_choice = input("Select a Sale ID: ")
    selected_sale = """
                    (select u.email, count(select reviewer from reviews, sales where reviewee = lister), avg(r.rating), s.descr, s.edate, s.cond, max(b.amount)
                    from sales s, reviews r, bids b, users u
                    where s.sid = ?
                    and u.email = s.lister
                    and u.email = r.reviewee
                    and s.lister = r.reviewee
                    and s.sid = b.sid)
                    union
                    (select u.email, count(select reviewer from reviews, sales where reviewee = lister), avg(r.rating), s.descr, s.edate, s.cond, s.rprice
                    from sales s, reviews r, users u
                    where s.sid = ?
                    and u.email = s.lister
                    and u.email = r.reviewee
                    and s.lister = r.reviewee);
                    """
    db.cur.execute(selected_sale, sID_choice, sID_choice)

    # NEED TO FINISH PRINTING OUT QUERY RESULTS

    print("""
            What would you like to do with this selection?
            1. Place bid on the selected sale
            2. List reviews of the product
            3. List review of the seller
            """)
    action = input("Select an action (1, 2, or 3): ")
    if action == "1":
        place_bid(sID_choice)
    elif action == "2":
        pass
    elif action == "3":
        pass
    else: 
        print("Invalid selection.") 



def active_sales(pID_choice):
    # List all active sales associated to the product, ordered based on the remaining time of the sale; includes the sale description, the maximum bid (if there is a bid on the item) or the reserved price (if there is no bid on the item), and the number of days, hours and minutes left until the sale expires
    clear_screen()
    sale_listing = """
                    (select s.sid s.descr, max(b.amount), datetime("s.edate") - datetime("now")
                    from sales s, bids b
                    where s.sid = b.sid
                    and s.pid = "{pid_1}"
                    and (datetime("s.edate") - datetime("now")) > 0)
                    union
                    (select s.sid s.descr, s.rprice, datetime("s.edate") - datetime("now")
                    from sales s
                    where (datetime("s.edate") - datetime("now")) > 0
                    and s.pid = "{pid_2}"
                    and not exists (select * from bids b, sales s 
                                    where b.sid = s.sid));
                    """
                    # 2nd query: selecting the rprice of sales if there isn't a bid for the product
    sale_query = sale_listing.format(pid_1=pID_choice, pid_2=pID_choice)
    db.cur.execute(sale_query) # query, placeholder, placeholder 
    rows = db.cur.fetchall()
    print("{:8}{:22}{:24}{:29}".format("Sale ID","Sale Description", "Max. Bid/Reserved Price", "Time Left Before Sale Expires"))
    print("{}".format("+" * 90))
    for row in rows:
        print("{sid:8}{description:22}{maxbid_rprice:24}{time_left}".format(sid = row[0], description = row[1], maxbid_rprice = row[2], time_left = row[3]))
    
    sale_select()

def sale_search():
    # Prompts user to enter keywords to use to compare to descriptions in query
    # Prints out the results
    search = input("Enter keywords to search for active sales: ")
    search_input = "%" + search + "%"
    search_listing = """
                    (select s.sid s.descr, max(b.amount), datetime("s.edate") - datetime("now")
                    from sales s, bids b
                    where s.sid = b.sid
                    and (datetime("s.edate") - datetime("now")) > 0)
                    and s.descr like ?
                    union
                    (select s.sid s.descr, s.rprice, datetime("s.edate") - datetime("now")
                    from sales s
                    where (datetime("s.edate") - datetime("now")) > 0
                    and s.descr like ?
                    and not exists (select * from bids b, sales s 
                                    where b.sid = s.sid));
                    """
                    # 2nd query: selecting the rprice of sales if there isn't a bid for the product
                    # need to figure out how to order the results??

    db.cur.execute(search_listing, (search_input, search_input,))
    rows = db.cur.fetchall()
    print("{:8}{:22}{:24}{:29}".format("Sale ID","Sale Description", "Max. Bid/Reserved Price", "Time Left Before Sale Expires"))
    print("{}".format("+" * 90))
    for row in rows:
        print("{sid:8}{description:22}{maxbid_rprice:24}{time_left}".format(sid = row[0], description = row[1], maxbid_rprice = row[2], time_left = row[3]))
    sale_select()

def print_sales(list):
    # Prints all the sales that are posted by the user
    # Takes in the list of tuples to be printed
    pass

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
    db.cur.execute("INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)", (sid, db.cur_user.get_email(), edate, desc, cond, r_price))

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
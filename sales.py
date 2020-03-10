# Need to figure out imports and how to get files to work together properly
import sqlite3
from main import cur, conn
from external_func import clear_screen
from datetime import datetime
from user import User

def place_bid(sID_choice):
    global user
    print("Placing a bid for {}:".format(sID_choice))

    bID = cur.execute("select count(*) from bids;")
    bidder = user.get_email()
    bdate = datetime.now()
    amount = int(input("Enter a bid amount: "))

    data = (bID, bidder, sID_choice, bdate, amount)
    cur.execute("insert into bids (?, ?, ?, ?, ?);", data)
    cur.commit()

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
    cur.execute(selected_sale, sID_choice, sID_choice)

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
                    and s.pid = ?
                    and (datetime("s.edate") - datetime("now")) > 0)
                    union
                    (select s.sid s.descr, s.rprice, datetime("s.edate") - datetime("now")
                    from sales s
                    where (datetime("s.edate") - datetime("now")) > 0
                    and s.pid = ?
                    and not exists (select * from bids b, sales s 
                                    where b.sid = s.sid));
                    """
                    # 2nd query: selecting the rprice of sales if there isn't a bid for the product

    cur.execute(sale_listing, pID_choice, pID_choice) # query, placeholder, placeholder 
    rows = cur.fetchall()
    print("{:8}{:22}{:24}{:29}".format("Sale ID","Sale Description", "Max. Bid/Reserved Price", "Time Left Before Sale Expires"))
    print("{}".format("+" * 90))
    for row in rows:
        print("{sid:8}{description:22}{maxbid_rprice:24}{time_left}".format(sid = row[0], description = row[1], maxbid_rprice = row[2], time_left = row[3]))
    
    sale_select()

def sale_search():
    # Prompts user to enter keywords to use to compare to descriptions in query
    # Prints out the results
    search_input = input("Enter keywords to search for active sales: ")
    search_listing = """
                    (select s.sid s.descr, max(b.amount), datetime("s.edate") - datetime("now")
                    from sales s, bids b
                    where s.sid = b.sid
                    and (datetime("s.edate") - datetime("now")) > 0)
                    and s.descr like '%?%'
                    union
                    (select s.sid s.descr, s.rprice, datetime("s.edate") - datetime("now")
                    from sales s
                    where (datetime("s.edate") - datetime("now")) > 0
                    and s.descr like '%?%'
                    and not exists (select * from bids b, sales s 
                                    where b.sid = s.sid));
                    """
                    # 2nd query: selecting the rprice of sales if there isn't a bid for the product
                    # need to figure out how to order the results??

    cur.execute(search_listing, search_input, search_input)
    rows = cur.fetchall()
    print("{:8}{:22}{:24}{:29}".format("Sale ID","Sale Description", "Max. Bid/Reserved Price", "Time Left Before Sale Expires"))
    print("{}".format("+" * 90))
    for row in rows:
        print("{sid:8}{description:22}{maxbid_rprice:24}{time_left}".format(sid = row[0], description = row[1], maxbid_rprice = row[2], time_left = row[3]))
    sale_select()

def print_sales(list):
    # Prints all the sales that are posted by the user
    # Takes in the list of tuples to be printed
    pass
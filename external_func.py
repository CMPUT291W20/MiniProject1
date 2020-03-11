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

def get_sale_select(sID_choice):

    selected_sale = """
                    select s.lister, CASE WHEN numReviews IS NULL THEN 0 ELSE numReviews END, CASE WHEN avgRate IS NULL THEN 0 ELSE avgRate END,
                        s.descr, s.edate, s.cond, CASE WHEN maxBid IS NULL THEN s.rprice ELSE maxBid END, p.descr, previewCount, avgPrate
                    from sales s left join 
                    (select reviewee, count(*) as numReviews, avg(rating) as avgRate from reviews group by reviewee) r on r.reviewee = s.lister left join
                    (select sid, max(amount) as maxBid from bids group by sid) b on b.sid = s.sid left join
                    (select pid, count(*) as previewCount, avg(rating) as avgPrate from previews group by pid) pr on pr.pid = s.pid left join
                    products p on p.pid = s.pid
                    where s.sid = "{sid}"
                    """
    selected_sale_query = selected_sale.format(sid=sID_choice)
    db.cur.execute(selected_sale_query)
    row = db.cur.fetchone()

    if row[7] is None:
        prodDescr = "N/A"
    else:
        prodDescr = row[7]
    if row[8] is None:
        numPr = "No Review yet"
    else:
        numPr = row[8]
    if row[9] is None:
        avgPr = "No Review yet"
    else:
        avgPr = row[9]

    dashes = "-" * 180
    print(dashes)
    print("{:<22s}{:<12s}{:<12s}{:<27s}{:<18s}{:<11s}{:<15s}{:<20s}{:<21s}{:<20s}".format("Lister", "Num Reviews", "Avg Rating", "Description", "End Date&Time", "Condition", "Highest Price", 
                                                                        "Product Description", "Num Product Reviews", "Avg Product Rating"))
    print(dashes)
    print("{:<22s}{:^12f}{:^12f}{:<27s}{:<18s}{:<11s}{:<15f}{:^20}{:^21}{:^20}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6], prodDescr, numPr, avgPr))

    return row

def print_active_sale(rows):
    dashses = "-" * 90
    print(dashses)
    print("{:<7}{:<9}{:<22}{:<25}{:<29}".format("Index","Sale ID","Sale Description", "Max. Bid/Reserved Price", "Time Left Before Sale Expires"))
    print(dashses)
    for i in range(len(rows)):
        #print("{sid:8}{description:22}{maxbid_rprice:24}{time_left}".format(sid = row[0], description = row[1], maxbid_rprice = row[2], time_left = row[3]))
        print("{:^7}{:^9s}{description:<22}{maxbid_rprice:^25}".format(i, rows[i][0], description = rows[i][1], maxbid_rprice = rows[i][2]))

    valid_index = False
    while not valid_index:
        try:
            index = int(input("Select a index for the sale: "))
            if index <= len(rows)-1 and index >= 0:
                valid_index = True
            else:
                print("Invalid index selected")
        except ValueError:
            print("Invalid index selected")
    return index
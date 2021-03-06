import os, sys
import database as db
import random
from datetime import datetime

def clear_screen():
    # Clears the terminal screen

    if sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("clear")

def close_program():
    # Displays a goodbye message and closes the program

    clear_screen()
    print("Thank you for shopping with us")
    print("Exiting Program....")
    sys.exit()

def place_bid(sID_choice, maxAmt):
    # Takes in a selected sale ID and the current max amount for that sale
    # Promps the user to enter in amount greater that the current maxAmt

    print("Placing a bid for {}:".format(sID_choice))

    valid_input =  False
    while not valid_input:
        print("Enter a bid ammount or type back.")
        amount = input("Amount: ")
        if amount == "back":
            valid_input = True
        else:
            try:
                if int(amount) <= maxAmt:
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

                    data = (bID, bidder, sID_choice, bdate, int(amount))
                    db.cur.execute("INSERT INTO bids VALUES (?, ?, ?, ?, ?)", data)
                    db.conn.commit()
            except ValueError:
                print("Invalid ammount entered")

def get_sale_select(sID_choice):
    # Takes in the a string sale ID to retrieve more data regarding that sale
    # Returns a row that contains the detailed sale information

    selected_sale = """
                    select s.lister, CASE WHEN numReviews IS NULL THEN 0 ELSE numReviews END, CASE WHEN avgRate IS NULL THEN 0 ELSE avgRate END,
                        s.descr, s.edate, s.cond, CASE WHEN maxBid IS NULL THEN (CASE WHEN s.rprice IS NULL THEN 0 ELSE s.rprice END) ELSE maxBid END, 
                        p.descr, previewCount, avgPrate
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
    # Takes in a list of tuples of active sale data to be formated and printed to the screen
    # After the print, prompt the user to select an index for futher action
    #   Return: index

    dashses = "-" * 90
    print(dashses)
    print("{:<7}{:<9}{:<22}{:<25}{:<29}".format("Index","Sale ID","Sale Description", "Max. Bid/Reserved Price", "Time Left Before Sale Expires"))
    print(dashses)
    for i in range(len(rows)):
        dt_list = rows[i][3].split()
        dates = dt_list[0].split("-")
        time = dt_list[1].split(":")
        a = datetime(int(dates[0]),int(dates[1]),int(dates[2]), int(time[0]), int(time[1]))

        dt_list = rows[i][4].split()
        dates = dt_list[0].split("-")
        time = dt_list[1].split(":")
        b = datetime(int(dates[0]),int(dates[1]),int(dates[2]), int(time[0]), int(time[1]))
        diff = str(a-b)
        print("{:^7}{:^9s}{description:<22}{maxbid_rprice:^25}{difference:^29}".format(i, rows[i][0], description = rows[i][1], maxbid_rprice = rows[i][2], difference = diff))

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
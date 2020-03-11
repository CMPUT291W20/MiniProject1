import sqlite3, random
import database as db
from external_func import clear_screen
from user import User
from sales import active_sales
from datetime import date

def write_preview(pID_choice):
    # Prompts user to fill in a rating and review text for the selected product
    # Fills in other required fields such as rid, reviewer, and rdate
    print("Writing a product review for {}:".format(pID_choice))
    
    valid_input = False
    while not valid_input:
        rating = int(input("Give the product a rating from 1 to 5: "))
        if rating in range(1,6): #to include 5
            valid_input = True
        else:
            print("Rating out of allowed range.")

    valid_input = False
    while not valid_input:
        review_text = input("Write your review (MAX 20 char): ")
        if len(review_text) <= 20:
            valid_input = True
        else:
            print("Max 20 characters allowed.")
    
    valid_rID = False
    while not valid_rID:
        rID = random.randint(1,999999999)
        db.cur.execute("select * from previews where rid = ?", (str(rID),))
        returned = db.cur.fetchone()
        if not returned:
            valid_rID = True
    
    reviewer = db.cur_user.get_email()
    today = date.today()
    r_date = today.strftime("%Y-%m-%d")
    
    data = (rID, pID_choice, reviewer, rating, review_text, r_date)
    print(data)
    db.cur.execute("INSERT INTO previews VALUES (?, ?, ?, ?, ?, ?)", data)
    db.conn.commit()


def list_preview(pID_choice):
    # Prints out the list of reviews of the selected product
    db.cur.execute("select * from previews where pid = ?", (pID_choice,))
    rows = db.cur.fetchall()
    
    if rows: 
        # There are tuples in list
        dashes = "-" * 90
        print(dashes)
        print("{:<12s}{:<12s}{:<22s}{:<8s}{:<22s}{:<11s}".format("Review ID", "Product ID", "Reviewer", "Rating", "Review Text", "Review Date"))
        print(dashes)
        for row in rows:
            print("{rid:^12}{pid:^12}{reviewer:<22}{rating:^8}{rtext:<22}{rdate:<11}".format(rid = row[0], pid = row[1], reviewer = row[2], rating = row[3], rtext = row[4], rdate = row[5]))
    else: 
        # There are no tuples in list
        print("This product has no reviews.")

    input("Press enter to return to the product listings: ")


def list_products():
    # Printing the product listing w/active sales (product id, description, number of reviews, average rating and # of active sales of product (active sale: sale end date and time has not reached yet))
    # Prompts user to select a product ID
    # Prompts user to select an action: write a product review, list all the product's reviews, list all active sales associated to the product
    finished = False
    while not finished:    
        clear_screen()
        product_listing = """
                    select p.pid, p.descr, CASE WHEN prCount IS NULL THEN 0 ELSE prCount END, CASE WHEN aRating IS NULL THEN 0 ELSE aRating END, activeC
                    from products p left join (select pid, count(*) as prCount, avg(rating) as aRating from previews group by pid) pr on p.pid = pr.pid
                    left join (select pid, count(*) as activeC from sales where edate > datetime('now') group by pid) s on p.pid = s.pid
                    where activeC > 0
                    order by activeC desc
                     """
        db.cur.execute(product_listing)
        rows = db.cur.fetchall()
        dashes = "-" * 80
        print(dashes)
        print("{:<7s}{:<12s}{:<22s}{:<14s}{:<16s}{:<12s}".format("Index","Product ID", "Description", "Review Count", "Average Rating", "Active Sales"))
        print(dashes)
        for i in range(len(rows)):
            print("{:^7d}{pid:^12}{descr:<22}{r_count:^14}{avg_rating:^16}{sale_count:^12}".format(i, pid = rows[i][0], descr = rows[i][1], r_count = rows[i][2], avg_rating = rows[i][3], sale_count = rows[i][4]))

        valid_index = False
        while not valid_index:
            try:
                index = int(input("Select a index for the product: "))
                if index <= len(rows)-1 and index >= 0:
                    valid_index = True
                else:
                    print("Error: invalid index selected")
            except ValueError:
                print("Invalid index selected")
        pID_choice = rows[index][0]

        print("""
                What would you like to do with this selection?
                1. Write a product review
                2. List all reviews of the product
                3. List active sales associated with the product
                4. Return to Main Menu
                """)

        action = input("Select an action (1, 2, 3, or 4): ")
        if action == "1":
            write_preview(pID_choice)
        elif action == "2":
            list_preview(pID_choice)
        elif action == "3":
            active_sales(pID_choice)
        elif action == "4":
            finished = True
        else: 
           print("Invalid selection.") 
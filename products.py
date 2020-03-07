import sqlite3
from main import clear_screen, cur, conn
from user import User
from sales import active_sales
from datetime import datetime

def write_preview(pID_choice):
    # Prompts user to fill in a rating and review text for the selected product
    # Fills in other required fields such as rid, reviewer, and rdate
    global user
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
    
    rID = cur.execute("select count(*) from previews;") # counting the number of product reviews currently in database, and assigning that number as the rID to this upcoming review
    reviewer = user.get_email()
    rdate = datetime.now()
    
    data = (rID, pID_choice, reviewer, rating, review_text, rdate)
    cur.execute("insert into previews (?, ?, ?, ?, ?, ?);", data)
    conn.commit()

def list_preview(pID_choice):
    # Prints out the list of reviews of the selected product
    cur.execute("select * from previews where pid = ?;", pID_choice)
    rows = cur.fetchall()
    
    if rows: 
        # There are tuples in list
        print("{:12}{:12}{:22}{:8}{:22}{}".format("Review ID", "Product ID", "Reviewer", "Rating", "Review Text", "Review Date"))
        print("{}".format("+" * 90))
        for row in rows:
            print("{rid:12}{pid:12}{reviewer:22}{rating:8}{rtext:22}{rdate}".format(rid = row[0], pid = row[1], reviewer = row[2], rating = row[3], rtext = row[4], rdate = row[5]))
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
                    select pd.pid, pd.descr, count(pr.rid), avg(pr.rating), count(s.sid)
                    from products pd, previews pr, sales s
                    where s.edate > datetime('now')
                    and pd.pid = s.pid
                    and pd.pid = pr.pid
                    and s.pid = pr.pid
                    order by count(s.sid) desc;
                    """
        cur.execute(product_listing)
        rows = cur.fetchall()
        print("{:12}{:22}{:14}{:16}{:19}".format("Product ID", "Description", "Review Count", "Average Rating", "Active Sale Count"))
        print("{}".format("+" * 90))
        for row in rows:
            print("{pid:12}{descr:22}{r_count:14}{avg_rating:16}{sale_count:19}".format(pid = row[0], descr = row[1], r_count = row[2], avg_rating = row[3], sale_count = row[4]))

        pID_choice = input("Select a Product ID: ")
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
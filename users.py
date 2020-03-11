from external_func import clear_screen, place_bid
import re, random
import database as db
from datetime import date

def user_search():
    # Promps the user to enter a keyword for the user to search for in the name or city
    continueSearch = True

    while continueSearch:
        clear_screen()
        print("Enter in a keyword to find users by name or email or type '!back' to go back to main menu")
        search = input("Search: ")
        if search == "!back":
            continueSearch = False
        else:
            like_search = "%" + search + "%"
            db.cur.execute("SELECT DISTINCT email, name, city, gender FROM users WHERE email LIKE ? or name LIKE ? ", (like_search, like_search,))
            list = db.cur.fetchall()
            print(list)
            print_userSearch(list, search)
            if list:
                # There were users returned from the search
                user_select(list)
    return  # Return back to main menu


def print_userSearch(list, search):
    # Prints the results that were returned from the user search
    # Takes in a list of tuples of users data: (email, name, city, gender)

    clear_screen()
    if list:
        dash = '-' * 90
        print(dash)
        print('{:<6s} {:<20s} {:<20s} {:<16s} {:<6s}'.format("Index","Name", "Email", "City", "Gender"))
        print(dash)
        for i in range(len(list)):
            print('{:^6d} {:<20s} {:<20s} {:<16s} {:<6s}'.format(i, list[i][1], list[i][0], list[i][2], list[i][3]))
    else:
        print("No results returned for your search " + search)


def user_select(list):
    # Promps user to select an operation for the user list printed
    # Takes in a list of tuples of users data: (email, name, city, gender)

    back = False
    while not back:
        valid_index = False
        while not valid_index:
            print("Please select an index from the list or type back to go back to search")
            index = input("Index: ")
            if index.lower() == "back":
                valid_index = True
                back = True
            elif int(index) <= len(list)-1:
                valid_index = True
            else:
                print("Error: Invalid Index selected")

        if not back:
            print("Please select an operation to")
            print("1. Write a review  2. List all user's active sales  3. List all reviews on user")
            valid_entry = False
            while not valid_entry:
                select = input("Selection: ")
                email = list[int(index)][0]  # User of the email selected
                if select == "1":
                    valid_entry = True
                    write_review(email)
                elif select == "2":
                    valid_entry = True
                    print_active_sales(email)
                elif select == "3":
                    valid_entry = True
                    print_reviews(email)
                else:
                    print("Invalid selection made")
            print_userSearch(list, None)
    return  # Return back to search for users


def write_review(email):
    # Promps user to enter review text and a rating (from 1 to 5)
    # Fills in the other required field of date, reviewer, reviewee
    clear_screen()

    if email == db.cur_user.get_email():
        print("You cannot write a review for yourself.")
        input("Press Enter to go back")
    else:
        print("Currently writing a review for: " + str(email))

        valid_input = False
        while not valid_input:
            r_text = input("Review Text (max 20 char): ")
            if len(r_text) <= 20:
                valid_input = True
            else:
                print("Error: Max 20 characters allowed")
        
        valid_input =  False
        while not valid_input:
            r_rating = input("Rating (1 to 5): ")
            if re.match("^[1-5]*$", r_rating):
                if int(r_rating) <= 5:
                    valid_input =  True
                    r_rating = int(r_rating)
                else:
                    print("Invalid Input")
            else:
                print("Invalid Input")

        today = date.today()
        r_date = today.strftime("%Y-%m-%d")
        db.cur.execute("INSERT INTO reviews VALUES (?, ?, ?, ?, ?)", (db.cur_user.get_email(), email, r_rating, r_text, r_date))
        db.conn.commit()


def print_reviews(email):
    # Prints all the reviews that are associated with the user
    # Takes in the email whom's reviews are to be printed

    clear_screen()
    db.cur.execute("SELECT * FROM reviews WHERE reviewee=?", (email,))
    list = db.cur.fetchall()
    if list:
        # There are tuples in the list
        dash = '-' * 90
        print(dash)
        print('{:<22s} {:<22s} {:<7s} {:<22s} {:<10s}'.format("Reviewer", "Reviewee", "Rating", "Description", "Date"))
        print(dash)
        for i in range(len(list)):
            print('{:<22s} {:<22s} {:.2f} {:<22s} {:<10s}'.format(list[i][0], list[i][1], list[i][2], list[i][3], list[i][4]))
    else:
        # There are no tuples in the list
        print("This user has no reviews")
    input("Press Enter to go back")


def print_active_sales(email):
    clear_screen()
    sale_listing = """
                    select s.sid, s.descr, CASE WHEN maxAmt IS NULL THEN s.rprice ELSE maxAmt END
                    from sales s left join 
                    (select sid, max(amount) as maxAmt from bids group by sid) b on b.sid = s.sid
                    where s.lister = "{e}"
                    and s.edate > datetime('now')
                    """
    sale_query = sale_listing.format(e=email)
    db.cur.execute(sale_query)
    rows = db.cur.fetchall()
    
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
    user_sale_select(rows[index][0])


def user_sale_select(selected_sid):

    selected_sale = """
                    select s.lister, CASE WHEN numReviews IS NULL THEN 0 ELSE numReviews END, CASE WHEN avgRate IS NULL THEN 0 ELSE avgRate END,
                        s.descr, s.edate, s.cond, CASE WHEN maxBid IS NULL THEN s.rprice ELSE maxBid END
                    from sales s left join 
                    (select reviewee, count(*) as numReviews, avg(rating) as avgRate from reviews group by reviewee) r on r.reviewee = s.lister left join
                    (select sid, max(amount) as maxBid from bids group by sid) b on b.sid = s.sid
                    where s.sid = "{sid}"
                    """
    selected_sale_query = selected_sale.format(sid=selected_sid)
    db.cur.execute(selected_sale_query)
    row = db.cur.fetchone()

    dashes = "-" * 110
    print(dashes)
    print("{:<22s}{:<12s}{:<12s}{:<27s}{:<18s}{:<11s}{:<15s}".format("Lister", "Num Reviews", "Avg Rating", "Description", "End Date&Time", "Condition", "Highest Price"))
    print(dashes)
    print("{:<22s}{:^12f}{:^12f}{:<27s}{:<18s}{:<11s}{:<15f}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))


    print("""
            What would you like to do with this selection?
            1. Place bid on the selected sale
            2. List all active sales by seller
            3. List reviewes of the seller
            """)
    action = input("Select an action (1, 2, or 3): ")
    if action == "1":
      place_bid(selected_sid, row[6])
    elif action == "2":
        print_active_sales(row[0])
    elif action == "3":
        print_reviews(row[0])
    else: 
        print("Invalid selection.") 
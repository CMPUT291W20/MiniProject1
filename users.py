def user_search():
    # Promps the user to enter a keyword for the user to search for in the name or city
    global cur
    continueSearch = True

    while continueSearch:
        print("Enter in a keyword to find users by name or email or type '!back' to go back to main menu")
        search = input("Search: ")
        if search == "!back":
            continueSearch = False
        else:
            list = cur.execute("SELECT name, email, city, gender FROM users WHERE email=? or name=?", (search, search,))
            print_userSearch(list, search)
            if list:
                # There were users returned from the search
                operation_select(list)
    return  # Return back to main menu


def print_userSearch(list, search):
    # Prints the results that were returned from the user search
    # Takes in a list of tuples of users data: (email, name, city, gender)

    if list:
        dash = '-' * 90
        print(dash)
        print('{:<6s} {:<20s} {:<20s} {:<16s} {:<6s}'.format("Index","Name", "Emai", "City", "Gender"))
        print(dash)
        for i in range(len(list)):
            print('{:^6d} {:<20s} {:<20s} {:<16s} {:<6s}'.format(i, list[i][1], list[i][0], list[i][2], list[i][3]))
    else:
        print("No results returned for your search " + search)


def operation_select(list):
    # Promps user to select an operation for the user list printed
    # Takes in a list of tuples of users data: (email, name, city, gender)

    print("Please select an index from the list or type back to go back to search")
    select = input("Selection: ")
    if select.lower() == "back":
        return
    else:
        print("1. Write a review  2. List all user's active sales  3. List all reviews on user")
        valid_entry = False
        while not valid_entry:
            select = int(input("Selection: "))
            email = list[select][0]  # User of the email selected
            if select == 1:
                valid_entry = True
                write_review(email)
            elif select == 2:
                valid_entry = True
                print_sales(email)
            elif select == 3:
                valid_entry = True
                print_reviews(email)
            else:
                print("Invalid selection made")
    return  # Return back to search for users


def write_review(email):
    # Promps user to enter review text and a rating (from 1 to 5)
    # Fills in the other required field of date, reviewer, reviewee
    global cur, conn
    pass

def print_sales(email):
    # Prints all the sales that are posted by the user
    # Takes in the email whom's sales are to be printed
    pass

def print_reviews(email):
    # Prints all the reviews that are associated with the user
    # Takes in the email whom's reviews are to be printed
    global cur

    cur.execute("SELECT * FROM reviews WHERE email=?", (email,))
    list = cur.fetchall()
    if list:
        # There are tuples in the list
        dash = '-' * 90
        print(dash)
        print('{:^6s}{:<22s} {:<22s} {:<7s} {:<22s} {:<10s}'.format("Index","Reviewer", "Reviewee", "Rating", "Description", "Date"))
        print(dash)
        for i in range(len(list)):
            print('{:^6d} {:<22s} {:<22s} {:^7d} {:<22s} {:<10s}'.format(i, list[i][0], list[i][1], list[i][2], list[i][3], list[i][4]))
    else:
        # There are no tuples in the list
        print("This user has no reviews")
class User:
    def __init__(self, email, name, city, gender):
        # Takes in email, name, city, gender to be set
        self.email = email
        self.name = name
        self.city = city
        self.gender = gender

    def get_email(self):
        # Return the users email
        return self.email

    def get_name(self):
        # Returns the users name
        return self.name

    def get_city(self):
        # Returns the users City
        return self.city

    def get_gender(self):
        # Returns the users Gender
        return self.gender
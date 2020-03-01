class User:
    def __init__(self, email, name, city, gender):
        self.email = email
        self.name = name
        self.city = city
        self.gender = gender

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

    def get_city(self):
        return self.city

    def get_gender(self):
        return self.gender
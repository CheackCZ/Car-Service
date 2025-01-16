import re

class Client():
    
    def __init__(self, id: int = 0, name: str = "", middle_name: str = "", last_name: str = "", phone: str = "", email: str = ""):
        """
        Initializes Client instance.

        :param id (int): ID of the client. Must be a non-negative integer.
        :param name (str): First name of the client. Optional, must be alphabetic if provided.
        :param middle_name (str): Middle name of the client. Optional, must be alphabetic if provided.
        :param last_name (str): Last name of the client. Optional, must be alphabetic if provided.
        :param phone (str): Phone number of the client. Optional, must match a valid phone format if provided.
        :param email (str): Email address of the client. Optional, must match a valid email format if provided.
        """
        # Validate id
        if type(id) != int or id < 0:
            raise ValueError("'id' must be a positive integer.")

        # Validate name (allow default empty string)
        if type(name) != str or len(name) > 50:
            raise ValueError("Name must be a string with a maximum of 50 characters.")

        # Validate middle name (allow default empty string)
        middle_name = middle_name or ""
        if type(middle_name) != str or len(middle_name) > 50:
            raise ValueError("Middle name must be a string with a maximum of 50 characters.")

        # Validate last name (allow default empty string)
        if type(last_name) != str or len(last_name) > 50:
            raise ValueError("Last name must be a string with a maximum of 50 characters.")


        # Validate phone (allow default empty string)
        if phone:
            if type(phone) != str or not phone.isdigit() or len(phone) not in range(9, 13):
                raise ValueError("Phone number must be a string of 9 to 12 digits.")
            
            
            phone_regex = re.compile(r"^\+?\d{1,4}?[ -]?\(?\d{1,3}?\)?[ -]?\d{1,4}[ -]?\d{1,4}[ -]?\d{1,9}$")
            if not phone_regex.match(phone):
                raise ValueError("Phone number is not valid! Please re-enter a valid one.")

        # Validate email (allow default empty string)
        if email:
            if type(email) != str or "@" not in email or "." not in email.split("@")[-1]:
                raise ValueError("Email must be a valid email address.")
            
            email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            if not email_regex.match(email):
                raise ValueError("Email is not valid! Please re-enter a valid one.")

        self.id = id
        self.name = name
        self.middle_name = middle_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        
    def __str__(self):
        return f"({self.id}) {self.name} {self.middle_name} {self.last_name}, Ph: {self.phone}), Em: {self.email}"
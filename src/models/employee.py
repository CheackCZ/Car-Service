import re

class Employee():
    """
    Class representing individual Employees in the database.
    """
    
    def __init__(self, id: int = 0, name: str = "", middle_name: str = "", last_name: str = "", phone: str = "", email: str = "", is_free: bool = True):
        """
        Initializes Employee instance. 

        :param name (str): First name of the employee. Must be a non-empty alphabetic string.
        :param middle_name (str): Middle name of the employee. Optional, must be alphabetic if provided.
        :param last_name (str): Last name of the employee. Must be a non-empty alphabetic string.
        :param phone (str): Phone number of the employee. Must match a valid phone number format.
        :param email (str): Email address of the employee. Must match a valid email format.
        :param is_free (bool): Availability status of the employee.
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
        phone = phone or ""
        if phone:
            phone_regex = re.compile(r"^\+?\d{9,13}$")
            if not phone_regex.match(phone):
                raise ValueError("Phone number must be between 9 and 13 digits, optionally starting with '+'.")
        

        # Validate email (allow default empty string)
        email = email or ""
        if email:
            if type(email) != str or "@" not in email or "." not in email.split("@")[-1]:
                raise ValueError("Email must be a valid email address.") 
            
            email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            if not email_regex.match(email):
                raise ValueError("Email is not valid! Please re-enter a valid one.")
        
        # Validate is_free
        if type(is_free) != bool:
            raise ValueError("is_free must be a boolean value!")
        
        self.id = id
        self.name = name
        self.middle_name = middle_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.is_free = is_free
        
    
    def __str__(self):
         return f"({self.id}) {self.name} {self.middle_name} {self.last_name}, Ph. {self.phone}, Em: {self.email}, Free? {self.is_free}"
    
    def to_dict(self):
        """
        Converts the Employee object into a dictionary.
        """
        return {
            "name": self.name,
            "middle_name": self.middle_name if self.middle_name else "",
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "is_free" : self.is_free
        }
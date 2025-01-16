import re

class Employee():
    """
    Class representing individual Employees in the database.
    """
    
    def __init__(self, id: int, name: str, middle_name: str, last_name: str, phone: str, email: str, is_free: bool):
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
        if type(id) != int or id <= 0:
            raise ValueError("'id' must be a positive integer.")
        
        # Validate name
        if not name or type(name) != str or not name.isalpha():
            raise ValueError("First name must be a non-empty string containing only alphabetic characters.")

        # Validate middle_name
        if middle_name:
            # Allow alphabetic characters and optional period
            allowed_middle_name = re.match(r"^[a-zA-Z.]+$", middle_name)
            if not allowed_middle_name:
                raise ValueError("Middle name must contain only alphabetic characters and optionally a period (.) or None.")
        
        
        # Validate last_name
        if not last_name or type(last_name) != str or not last_name.isalpha():
            raise ValueError("Last name must be a non-empty string containing only alphabetic characters.")
        
         # Validate phone
        if not phone or type(phone) != str or not phone.isdigit() or len(phone) not in range(9, 13):
            raise ValueError(f"Phone phone must be a string of 10 or 11 digits.{phone}")
        
        phone_regex = re.compile(r"^\+?\d{1,4}?[ -]?\(?\d{1,3}?\)?[ -]?\d{1,4}[ -]?\d{1,4}[ -]?\d{1,9}$")
        if not phone_regex.match(phone):
            raise ValueError("Phone number is not valid! Please re-enter a valid one.")
        
        # Validate email
        if not email or type(name) != str or "@" not in email or "." not in email.split("@")[-1]:
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
import re

class Employee():
    """
    Class representing individual Employees in the database.
    """
    
    def __init__(self, id: int = 0, name: str = None, middle_name: str = None, last_name: str = None, phone: str = None, email: str = None, is_free: bool = True):
        """
        Initializes Employee instance.
        """
        # Core validation
        if id is not None and (type(id) != int or id < 0):
            raise ValueError("'id' must be a positive integer.")

        # Name validation (if provided)
        if name is not None:
            if not self._is_valid_czech_name(name):
                raise ValueError("Name must contain only alphabetic characters (including Czech letters) and be at most 50 characters long.")

        # Middle name validation (if provided)
        if middle_name is not None:
            if not self._is_valid_czech_name(middle_name, optional=True):
                raise ValueError("Middle name must contain only alphabetic characters (including Czech letters) and be at most 50 characters long.")

        # Last name validation (if provided)
        if last_name is not None:
            if not self._is_valid_czech_name(last_name):
                raise ValueError("Last name must contain only alphabetic characters (including Czech letters) and be at most 50 characters long.")

        # Phone validation (if provided)
        if phone is not None:
            if not re.match(r"^\+?\d{9,13}$", phone):
                raise ValueError("Phone number must be between 9 and 13 digits, optionally starting with '+'.")

        # Email validation (if provided)
        if email is not None:
            if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                raise ValueError("Email must be a valid email address.")

        if is_free is not None and type(is_free) != bool:
            raise ValueError("is_free must be a boolean value.")
        
        self.id = id
        self.name = name
        self.middle_name = middle_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.is_free = is_free
        
    
    def __str__(self):
         return f"({self.id}) {self.name} {self.middle_name} {self.last_name}, Ph. {self.phone}, Em: {self.email}, Free? {self.is_free}"
    
    
    def _is_valid_czech_name(self, value: str, optional: bool = False):
        """
        Validates if a name is valid (supports Czech characters).
        """
        if optional and not value:
            return True  
        if not isinstance(value, str) or len(value) > 50:
            return False
        return bool(re.match(r"^[a-zA-Zá-žÁ-Ž]+\.?$", value))
    
    def to_dict(self):
        """
        Converts the Employee object into a dictionary.
        """
        return {
            "name": self.name,
            "middle_name": self.middle_name or "",
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "is_free": self.is_free,
        }
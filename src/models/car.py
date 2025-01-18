from datetime import datetime
import re

from src.models.client import Client
from src.models.brand import Brand


class Car():
    """
    Class representing individual Cars in the database.
    """
    
    def __init__(self, id: int = 0, client: Client = Client(), brand: Brand = Brand(), registration_number: str = "", registration_date: datetime = None, model: str = ""):
        """
        Initializes a Car instance.
        
        :param id (int): The unique identifier for the car.
        :param client_id (int): The ID of the client who owns the car.
        :param brand_id (int): The ID of the brand of the car.
        :param registration_number (str): The registration number of the car.
        :param registration_date (date): The registration date of the car.
        :param model (str): The model name of the car.
        """
        # Validate id
        if type(id) != int or id < 0:
            raise ValueError("'id' must be a positive integer.")

        # Validate client
        if type(client) != Client:
            raise TypeError("'client' must be an instance of Client.")

        # Validate brand
        if type(brand) != Brand:
            raise TypeError("'brand' must be an instance of Brand.")

        # Validate registration_number
        if type(registration_number) != str:
            raise ValueError("'registration_number' must be a string.")
        if len(registration_number) > 10:
            raise ValueError("'registration_number' cannot exceed 15 characters.")

         # Skip regex validation for an empty registration_number
        if registration_number and not re.match(r"[A-Z0-9]{1,3}[- ]?[0-9]{1,4}", registration_number):
            raise ValueError("Registration number is not valid! Please re-enter a valid one.")


        # Validate registration_date
        if registration_date is None:
            registration_date = datetime.now() 
        elif not isinstance(registration_date, datetime):
            raise TypeError("'registration_date' must be a datetime object or None.")

        # Validate model
        if type(model) != str:
            raise ValueError("'model' must be a non-empty string.")
        if len(model) > 50:
            raise ValueError("'model' cannot exceed 50 characters.")
        
        self.id = id
        self.client = client
        self.brand = brand
        self.registration_number = registration_number.strip()
        self.registration_date = registration_date
        self.model = model.strip()
        
    def __str__(self):
        """
        Returns a string representation of the Car instance.

        :return str: A formatted string with the car's details.
        """
        return f"({self.id}) {self.brand} {self.model}, {self.registration_number} ({self.registration_date})"
    
    def to_dict(self):
        """
        Converts the Car object into a dictionary.
        """
        return {
            "id": self.id,
            "client_id" : self.client.id if self.client else None,
            "client_name": self.client.name if self.client else None,
            "client_last_name": self.client.last_name if self.client else None,
            "brand_name": self.brand.name,
            "registration_number": self.registration_number,
            "registration_date": self.registration_date.strftime("%Y-%m-%d") if self.registration_date else None,
            "model": self.model
        }
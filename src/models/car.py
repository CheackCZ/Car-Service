from datetime import datetime
import re

from src.models.client import Client
from src.models.brand import Brand


class Car():
    """
    Class representing individual Cars in the database.
    """
    
    def __init__(self, id: int, client: Client, brand: Brand, registration_number: str, registration_date: datetime, model: str):
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
        if type(id) != int or id <= 0:
            raise ValueError("'id' must be a positive integer.")

        # Validate client
        if type(client) != Client:
            raise TypeError("'client' must be an instance of Client.")

        # Validate brand
        if type(brand) != Brand:
            raise TypeError("'brand' must be an instance of Brand.")

        # Validate registration_number
        if type(registration_number) != str or not registration_number.strip():
            raise ValueError("'registration_number' must be a non-empty string.")
        if len(registration_number) > 10:
            raise ValueError("'registration_number' cannot exceed 15 characters.")

        registration_number_regex = re.compile(r"^[A-Z0-9]{1,3}[- ]?[A-Z0-9]{1,4}[- ]?[A-Z0-9]{1,4}$")
        if not registration_number_regex.match(registration_number):
            raise ValueError("Phone number is not valid! Please re-enter a valid one.")

        # Validate registration_date
        if type(registration_date) != datetime:
            raise TypeError("'registration_date' must be a datetime object.")

        # Validate model
        if type(model) != str or not model.strip():
            raise ValueError("'model' must be a non-empty string.")
        if len(model) > 50:
            raise ValueError("'model' cannot exceed 50 characters.")
        
        self.id = id
        self.client = client
        self.brand = brand
        self.registration_number = registration_number.strip()
        self.registration_date = registration_date
        self.model = model.strip()
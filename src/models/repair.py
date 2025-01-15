from enum import Enum
from datetime import datetime

from models.employee import Employee
from models.car import Car
from models.repair_type import RepairType

class State(Enum):
    """
    Enum representing the possible states of a repair.
    """
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    
class Repair():
    """
    Class representing individual Repairs in the database.
    """
    
    def __init__(self, id: int, car: Car, employee: Employee, repair_type: RepairType, date_started: datetime, date_finished: datetime, price: float, state: State):
        """
        Initializes Repair instance.

        :param car (Car): The car associated with the repair.
        :param employee (Employee): The employee performing the repair.
        :param repair_type (RepairType): The type of repair being performed.
        :param date_started (datetime): The datetime when the repair started.
        :param date_finished (datetime): The datetime when the repair finished (or is planned to finish).
        :param price (float): The price of the repair. Must be a non-negative float or integer.
        :param state (State): The current state of the repair, represented as an instance of the `State` enum.
        """
        # Validate id
        if type(id) != int or id <= 0:
            raise ValueError("'id' must be a positive integer.")
        
        # Validate car
        if type(car) != Car:
            raise TypeError("Car must be an instance of Car.")

        # Validate employee
        if type(employee) != Employee:
            raise TypeError("Employee must be an instance of Employee.")

        # Validate repair_type
        if type(repair_type) != RepairType:
            raise TypeError("Repair_type must be an instance of RepairType.")

        # Validate date_started
        if type(date_started) != datetime:
            raise TypeError("Date_started must be a datetime object.")

        # Validate date_finished
        if type(date_finished) != datetime:
            raise TypeError("Date_finished must be a datetime object.")
        
        if date_finished < date_started:
            raise ValueError("Date_finished cannot be earlier than date_started.")

        # Validate price
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative float or integer.")

        # Validate state
        if  type(repair_type) != State:
            raise TypeError("State must be an instance of State (Enum).")

        # Assign attributes
        self.id = id
        self.car = car
        self.employee = employee
        self.repair_type = repair_type
        self.date_started = date_started
        self.date_finished = date_finished
        self.price = price
        self.state = state
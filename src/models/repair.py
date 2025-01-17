from enum import Enum
from datetime import datetime

from src.models.employee import Employee
from src.models.car import Car
from src.models.repair_type import RepairType

class State(Enum):
    """
    Enum representing the possible states of a repair.
    """
    DEFAULT = "Pending"
    IN_PROGRESS = "In process"
    COMPLETED = "Done"
    CANCELED = "Canceled"
    
class Repair():
    """
    Class representing individual Repairs in the database.
    """
    
    def __init__(self, id: int = 0, car: Car = Car(), employee: Employee = Employee(), repair_type: RepairType = RepairType(), date_started: datetime = None, date_finished: datetime = None, price: float = 0, state: State = State.DEFAULT):
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
        if type(id) != int or id < 0:
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

        # Allow `date_finished` to be None or a `datetime` object
        if date_finished is not None and not isinstance(date_finished, datetime):
            raise TypeError("Date_finished must be a datetime object or None.")
        self.date_finished = date_finished

        # Validate price
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative float or integer.")

        # Validate state
        if type(state) != State:
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
        
    
    def __str__(self):
        return f"({self.id}) {self.car} | {self.employee} | {self.repair_type} | {self.date_started} -> {self.date_finished} | {self.price} | {self.state}"
        
    def to_dict(self):
        """
        Converts the Repair object into a dictionary representation,
        
        :return: Dictionary representation of the Repair object.
        """
        return {
            "id": self.id,
            "employee_name": f"{self.employee.name} {self.employee.last_name}",
            "employee_id": self.employee.id,  
            "car_model": self.car.model,
            "car_registration_num": self.car.registration_number,
            "brand_name": self.car.brand.name,
            "repair_type": self.repair_type.name,
            "date_started": self.date_started.strftime("%Y-%m-%d %H:%M:%S"),
            "date_finished": self.date_finished.strftime("%Y-%m-%d %H:%M:%S") if self.date_finished else "N/A",
            "price": self.price,
            "state": self.state.value
        } 
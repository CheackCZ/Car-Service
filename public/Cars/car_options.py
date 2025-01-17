from datetime import datetime

import customtkinter as ctk
from tkinter import ttk

from CTkMessagebox import CTkMessagebox

from src.models.car import Car
from src.models.client import Client
from src.models.brand import Brand

from src.controllers.car_controller import CarController

from public.Cars.car_dialog import CarDialog
from public.Cars.car_selector import CarSelector

class CarsOptions(ctk.CTkFrame):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(fg_color="transparent")

        # Label with "Options" 
        self.db_name_label = ctk.CTkLabel(self, text="Options:", font=("Poppins", 14), text_color="gray", wraplength=160, justify="left")
        self.db_name_label.place(x=10, y=10)

        # Add Button
        self.add_button = ctk.CTkButton(self, command=self.open_add_car_dialog, text="Add Car", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.add_button.place(x=10, y=50)

        # Edit Button
        self.edit_button = ctk.CTkButton(self, command=self.open_car_selector_for_edit, text="Edit Car", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.edit_button.place(x=10, y=90)

        # Remove Button
        self.remove_button = ctk.CTkButton(self, text="Remove Car", command=self.open_car_selector_for_remove, border_width=2, border_color="#FF474D", hover_color="red", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.remove_button.place(x=10, y=130)

        # Separator
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.place(x=10, y=180, width=140)

        # Toggle Switch for Dirty Reading
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self, text="Dirty Reading", variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.place(x=20, y=200)
        

    def open_add_car_dialog(self):
        """
        Opens the dialog to add a new car.
        """
        dialog = CarDialog(self, on_submit_callback=self.handle_add_car, mode="add")
        dialog.grab_set()
        dialog.lift()

    def handle_add_car(self, car_data):
        """
        Handles adding a new car to the database.
        """
        try:
            client_id = int(car_data["client_id"])
            brand_id = int(car_data["brand_id"])  

            # Create a new Car object
            new_car = Car(
                client=Client(id=client_id),
                brand=Brand(id=brand_id),
                registration_number=car_data["registration_number"],
                registration_date=car_data["registration_date"],
                model=car_data["model"]
            )

            # Save the car
            CarController.insert(new_car)
            CTkMessagebox(title="Success", message="Car added successfully.", icon="info")
        except Exception as e:
            print(e)
            CTkMessagebox(title="Error", message=f"Failed to add car: {e}", icon="warning")


    def open_car_selector_for_edit(self):
        """
        Opens the car selector to choose a car for editing.
        """
        selector = CarSelector(parent=self, on_submit_callback=self.open_edit_car_dialog, title="Edit Car", button_text="Edit Car")
        selector.grab_set()
        selector.lift()

    def open_edit_car_dialog(self, car_id):
        """
        Opens the dialog to edit a selected car.
        """
        try:
            car = CarController.fetch_by_id(car_id)
            if not car:
                print("Car not found.")
                return

            car_data = car.to_dict()
            dialog = CarDialog(self, on_submit_callback=self.handle_edit_car, mode="edit", car_data=car_data)
            dialog.grab_set()
            dialog.lift()
        except Exception as e:
            print(f"Failed to fetch car: {e}")

    def handle_edit_car(self, car_data):
        """
        Handles editing an existing car in the database.
        """
        try:
            # Extract client ID and brand name from car_data
            car_id = car_data["id"]
            client_id = int(car_data["client_id"])
            brand_id = int(car_data["brand_id"])

            # Create and update the Car object
            updated_car = Car(
                id=car_id,
                client=Client(id=client_id),
                brand=Brand(id=brand_id),
                registration_number=car_data["registration_number"],
                registration_date=car_data["registration_date"],
                model=car_data["model"]
            )
            CarController.update(updated_car)
            CTkMessagebox(title="Success", message="Car updated successfully.", icon="info")
        except Exception as e:
            print(e)
            CTkMessagebox(title="Error", message=f"Failed to update car: {e}", icon="warning")


    def open_car_selector_for_remove(self):
        """
        Opens the car selector to choose a car for removal.
        """
        selector = CarSelector(
            parent=self,
            on_submit_callback=self.handle_remove_car,
            title="Remove Car",
            button_text="Remove Car"
        )
        selector.lift()
        selector.grab_set()

    def handle_remove_car(self, car_id):
        """
        Handles removing a car from the database.
        """
        try:
            CarController.delete(car_id)
            CTkMessagebox(title="Success", message="Car deleted successfully.", icon="info")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"{e}", icon="warning")
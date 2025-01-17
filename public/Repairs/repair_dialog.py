from datetime import datetime

import customtkinter as ctk
from tkinter import ttk

from CTkMessagebox import CTkMessagebox

from src.models.repair import State

from src.controllers.repair_type_controller import RepairTypeController
from src.controllers.employee_controller import EmployeeController
from src.controllers.car_controller import CarController

class RepairDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_submit_callback, mode="add", repair_data=None, **kwargs):
        super().__init__(**kwargs)

        self.mode = mode
        self.repair_data = repair_data if repair_data else {}

        # Set title and window properties
        title_text = "Add Repair" if self.mode == "add" else "Edit Repair"
        self.title(title_text)
        self.geometry("360x420")
        self.resizable(False, False)

        self.parent = parent
        self.on_submit_callback = on_submit_callback

        # Title Label
        self.title_label = ctk.CTkLabel(self, text=title_text, font=("Poppins", 16, "bold"), text_color="white")
        self.title_label.place(relx=0.5, y=30, anchor="center")

        # Combobox for Repair Type
        self.repair_type_label = ctk.CTkLabel(self, text="Repair Type:", font=("Poppins", 12, "bold"))
        self.repair_type_label.place(x=20, y=70)
        self.repair_type_combobox = ttk.Combobox(self, values=[])
        self.repair_type_combobox.place(x=150, y=70, width=190)

        # Combobox for Employee
        self.employee_label = ctk.CTkLabel(self, text="Employee:", font=("Poppins", 12, "bold"))
        self.employee_label.place(x=20, y=100)
        self.employee_combobox = ttk.Combobox(self, values=[])
        self.employee_combobox.place(x=150, y=100, width=190)

        # Combobox for Car
        self.car_label = ctk.CTkLabel(self, text="Car:", font=("Poppins", 12, "bold"))
        self.car_label.place(x=20, y=130)
        self.car_combobox = ttk.Combobox(self, values=[])
        self.car_combobox.place(x=150, y=130, width=190)

        # Date Picker for Start Date
        self.date_started_label = ctk.CTkLabel(self, text="Start Date:", font=("Poppins", 12, "bold"))
        self.date_started_label.place(x=20, y=180)
        self.date_started_entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD", width=190)
        self.date_started_entry.place(x=150, y=180)

        # Date Picker for End Date
        self.date_ended_label = ctk.CTkLabel(self, text="End Date:", font=("Poppins", 12, "bold"))
        self.date_ended_label.place(x=20, y=220)
        self.date_ended_entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD", width=190)
        self.date_ended_entry.place(x=150, y=220)

        # Price Input
        self.price_label = ctk.CTkLabel(self, text="Price (CZK):", font=("Poppins", 12, "bold"))
        self.price_label.place(x=20, y=270)
        self.price_entry = ctk.CTkEntry(self, placeholder_text="0.00", width=190)
        self.price_entry.place(x=150, y=270)

        # Combobox for State
        self.state_label = ctk.CTkLabel(self, text="State:", font=("Poppins", 12, "bold"))
        self.state_label.place(x=20, y=320)
        self.state_combobox = ttk.Combobox(self, values=[])
        self.state_combobox.place(x=150, y=320, width=190)

        # Submit Button
        self.submit_button = ctk.CTkButton(self, text=title_text, command=self.submit_form)
        self.submit_button.place(relx=0.5, y=380, anchor="center")

        self.load_comboboxes()
        self.fill_entries()

    
    def load_comboboxes(self):
        """
        Fetch repair types, employees, and cars from the database and populate the comboboxes.
        """
        try:
            # Load repair types
            repair_types = RepairTypeController.fetch_all()
            self.repair_type_combobox.configure(
                values=[f"({rt.id}) {rt.name}" for rt in repair_types]
            )

            # Load employees
            employees = EmployeeController.fetch_all()
            self.employee_combobox.configure(
                values=[f"({emp.id}) {emp.name} {emp.last_name}" for emp in employees]
            )

            # Load cars
            cars = CarController.fetch_all()
            self.car_combobox.configure(
                values=[f"({car.id}) {car.brand.name} {car.model} - {car.registration_number}" for car in cars]
            )

            # Load states from the State enum
            self.state_combobox.configure(
                values=[state.value for state in State]  
            )

        except Exception as e:
            print(f"Error loading comboboxes: {e}")


    def submit_form(self):
        """
        Collects data from the form and invokes the callback to handle submission.
        """
        try:
            repair_type_text = self.repair_type_combobox.get().strip()
            if repair_type_text:
                try:
                    repair_type_id = int(repair_type_text.split("(")[1].split(")")[0]) 
                except (IndexError, ValueError):
                    raise ValueError("Please select a valid repair type.")
            else:
                raise ValueError("Please select a repair type.")

            # Extract and validate employee ID
            employee_text = self.employee_combobox.get().strip()
            if employee_text:
                employee_id = int(employee_text.split("(")[1].split(")")[0])
            else:
                raise ValueError("Please select a valid employee.")

            # Extract and validate car ID
            car_text = self.car_combobox.get().strip()
            if car_text:
                car_id = int(car_text.split("(")[1].split(")")[0])
            else:
                raise ValueError("Please select a valid car.")

            # Validate and parse date_started
            date_started = self.date_started_entry.get().strip()
            if not date_started:
                raise ValueError("Start date is required.")
            try:
                date_started = datetime.strptime(date_started, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Start date must be in the format YYYY-MM-DD.")

            # Validate and parse date_ended (optional)
            date_ended = self.date_ended_entry.get().strip()
            if date_ended:
                try:
                    date_ended = datetime.strptime(date_ended, "%Y-%m-%d")
                    if date_ended < date_started:
                        raise ValueError("End date cannot be earlier than the start date.")
                except ValueError:
                    raise ValueError("End date must be in the format YYYY-MM-DD.")
            else:
                date_ended = None

            # Validate price
            try:
                price = float(self.price_entry.get().strip())
                if price < 0:
                    raise ValueError("Price cannot be negative.")
            except ValueError:
                raise ValueError("Price must be a valid number.")

            # Validate state
            state = self.state_combobox.get().strip()
            if state not in [s.value for s in State]:
                raise ValueError("Please select a valid state.")

            # Build repair data
            repair_data = {
                "id": self.repair_data.get("id", None),  # Use existing ID or None for new repairs
                "repair_type_id": repair_type_id,
                "employee_id": employee_id,
                "car_id": car_id,
                "date_started": date_started.strftime("%Y-%m-%d"),
                "date_ended": date_ended.strftime("%Y-%m-%d") if date_ended else None,
                "price": price,
                "state": state,
            }

            # Pass the data to the callback
            self.on_submit_callback(repair_data)

        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="warning")
            return

        # Close the dialog on successful submission
        self.destroy()


    def fill_entries(self):
        """
        Fills an entry widget with data from repair_data if in edit mode.
        """
        if self.mode == "edit":
            # Set repair type combobox value
            repair_type_name = self.repair_data.get("repair_type", "")
            if repair_type_name:
                for value in self.repair_type_combobox.cget("values"):
                    if repair_type_name in value:  
                        self.repair_type_combobox.set(value)
                        break

            # Set employee combobox value
            employee_id = self.repair_data.get("employee_id")
            if employee_id:
                for value in self.employee_combobox.cget("values"):
                    if value.startswith(f"({employee_id})"):  
                        self.employee_combobox.set(value)
                        break

            car_registration_num = self.repair_data.get("car_registration_num", "")
            car_model = self.repair_data.get("car_model", "")
            if car_registration_num and car_model:
                for value in self.car_combobox.cget("values"):
                    if car_registration_num in value and car_model in value:  
                        self.car_combobox.set(value)
                        break
                    
            self.date_started_entry.insert(0, self.repair_data.get("date_started", ""))
            self.date_ended_entry.insert(0, self.repair_data.get("date_finished", ""))
            self.price_entry.insert(0, self.repair_data.get("price", ""))
            self.state_combobox.set(self.repair_data.get("state", ""))

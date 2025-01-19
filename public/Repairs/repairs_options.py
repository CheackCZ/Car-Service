from datetime import datetime, date

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from tkinter import ttk

from src.models.repair_type import RepairType
from src.models.employee import Employee
from src.models.car import Car
from src.models.repair import Repair, State
from src.models.dirty_reading import DirtyReading

from src.controllers.dirty_reading_controller import DirtyReadingController

from public.Repairs.repair_dialog import RepairDialog
from public.Repairs.repair_selector import RepairSelector


class RepairsOptions(ctk.CTkFrame):
    """
    A frame providing options for managing repairs, such as adding, editing, and removing repairs.
    """
    
    def __init__(self, parent, session_id, controller, car_controller, employee_controller, repair_type_controller, **kwargs):
        """
        Initialize the RepairsOptions frame.
        
        :param parent: The parent widget.
        :param **kwargs: Additional keyword arguments for the frame configuration.
        """
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")

        self.session_id = session_id
        
        self.repair_controller = controller
        self.employee_controller = employee_controller
        self.car_controller = car_controller
        self.repair_type_controller = repair_type_controller

        # Label with "Options" 
        self.db_name_label = ctk.CTkLabel(self, text="Options:", font=("Poppins", 14), text_color="gray", wraplength=160, justify="left")
        self.db_name_label.place(x=10, y=10)

        # Add Button
        self.add_button = ctk.CTkButton(self, command=self.open_add_repair_dialog, text="Add Repair", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.add_button.place(x=10, y=50)

        # Edit Button
        self.edit_button = ctk.CTkButton(self, command=self.open_repair_selector_for_edit, text="Edit Repair", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.edit_button.place(x=10, y=90)

        # Remove Button
        self.remove_button = ctk.CTkButton(self, text="Remove Repair", command=self.open_repair_selector_for_remove, border_width=2, border_color="#FF474D", hover_color="red", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.remove_button.place(x=10, y=130)

        # Separator
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.place(x=10, y=180, width=140)

        # Toggle Switch for Dirty Reading
        self.switch_var = ctk.StringVar(value=self.get_dirty_reading_value("repair"))
        self.switch = ctk.CTkSwitch(self, text="Dirty R/W", variable=self.switch_var, onvalue='1', offvalue='0', command=self.toggle_dirty_reading)
        self.switch.place(x=20, y=200)
        

    def open_add_repair_dialog(self):
        """
        Opens the dialog to add a new repair.
        """
        dialog = RepairDialog(self, on_submit_callback=self.handle_add_repair, mode="add", controller=self.repair_controller, car_controller=self.car_controller, employee_controller=self.employee_controller, repair_type_controller=self.repair_type_controller)
        dialog.grab_set()
        dialog.lift()

    def handle_add_repair(self, repair_data):
        """
        Handles adding a new repair to the database.
        
        :param repair_data (dict): Data for the new repair.
        """
        print(repair_data)

        try:
            # Extract and parse data
            repair_type_id = repair_data["repair_type_id"]
            car_id = repair_data["car_id"]
            employee_id = repair_data["employee_id"]
            date_started = datetime.strptime(repair_data["date_started"], "%Y-%m-%d").date()

            # Validate and handle date_finished based on the state
            state = State(repair_data["state"])
            if state in [State("Pending"), State("In process")]:
                date_finished = None  # Allow None for these states
            else:
                # Raise an error if date_finished is empty for invalid states
                if not repair_data.get("date_ended"):
                    raise ValueError("Date finished cannot be empty for state 'Completed' or 'Canceled'.")
                date_finished = datetime.strptime(repair_data["date_ended"], "%Y-%m-%d").date()

            # Create a new Repair object
            new_repair = Repair(
                repair_type=RepairType(id=repair_type_id),
                employee=Employee(id=employee_id),
                car=Car(id=car_id),
                date_started=date_started,
                date_finished=date_finished,
                price=repair_data["price"],
                state=state
            )

            # Insert the repair into the database
            self.repair_controller.insert(new_repair)
            CTkMessagebox(title="Success", message="Repair added successfully.", icon="info")
        except ValueError as ve:
            print(f"Validation Error: {ve}")
            CTkMessagebox(title="Validation Error", message=str(ve), icon="warning")
        except Exception as e:
            print(e)
            CTkMessagebox(title="Error", message=f"Failed to add repair: {e}", icon="warning")


    def open_repair_selector_for_edit(self):
        """
        Opens the repair selector to choose a repair for editing.
        """
        selector = RepairSelector(parent=self, on_submit_callback=self.open_edit_repair_dialog, title="Edit Repair", button_text="Edit Repair", controller=self.repair_controller)
        selector.grab_set()
        selector.lift()
        

    def open_edit_repair_dialog(self, repair_id):
        """
        Opens the dialog to edit a selected repair.
        
        :param repair_id (int): ID of the repair to edit.
        """
        try:
            repair = self.repair_controller.fetch_by_id(repair_id)
            if not repair:
                CTkMessagebox(title="Error", message="Repair not found.", icon="warning")
                return

            repair_data = repair.to_dict()
            dialog = RepairDialog(self, on_submit_callback=self.handle_edit_repair, controller=self.repair_controller, car_controller=self.car_controller, employee_controller=self.employee_controller, repair_type_controller=self.repair_type_controller, mode="edit", repair_data=repair_data)
            dialog.grab_set()
            dialog.lift()
            
        except Exception as e:
            print(f"Failed to fetch repair: {e}")

    def handle_edit_repair(self, repair_data):
        """
        Handles editing an existing repair in the database.
        
        :param repair_data (dict): Updated data for the repair.
        """
        try:
            repair_type_id=repair_data["repair_type_id"]
            car_id = repair_data["car_id"]
            employee_id=repair_data["employee_id"]
            
            state_enum = State(repair_data["state"])
            
             # Parse date_ended, handle "N/A" or None
            if repair_data["date_ended"] and repair_data["date_ended"] != "N/A":
                date_finished = datetime.strptime(repair_data["date_ended"], "%Y-%m-%d").date()
            else:
                date_finished = None
            
            updated_repair = Repair(
                id=repair_data["id"],
                repair_type=RepairType(id=repair_type_id),
                employee=Employee(id=employee_id),
                car=Car(id=car_id),
                date_started=datetime.strptime(repair_data["date_started"], "%Y-%m-%d").date(),
                date_finished=date_finished,
                price=repair_data["price"],
                state=state_enum             
            )
            
            record = DirtyReadingController.fetch_by_table_name("repair")
            if record:
                self.repair_controller.update(updated_repair, False)
            else:
                self.repair_controller.update(updated_repair,True)
    
            CTkMessagebox(title="Success", message="Repair updated successfully.", icon="info")
        except Exception as e:
            print(e)
            CTkMessagebox(title="Error", message=f"Failed to edit repair: {e}", icon="warning")


    def open_repair_selector_for_remove(self):
        """
        Opens the repair selector to choose a repair for removal.
        """
        selector = RepairSelector(parent=self, on_submit_callback=self.handle_remove_repair, title="Remove Repair", button_text="Remove Repair", controller=self.repair_controller)
        selector.grab_set()
        selector.lift()

    def handle_remove_repair(self, repair_id):
        """
        Handles removing a repair from the database.
        
        :param repair_id (int): ID of the repair to remove.
        """
        try:
            repair = self.repair_controller.fetch_by_id(repair_id)
            if not repair:
                raise ValueError("Repair not found.")
            
            # Check the repair state
            if repair.state not in [State.COMPLETED, State.CANCELED]:
                raise ValueError("Only repairs marked as 'Completed' or 'Canceled' can be deleted.")
            
            self.repair_controller.delete(repair_id)
            CTkMessagebox(title="Success", message="Repair deleted successfully.", icon="info")
        except Exception as e:
            CTkMessagebox(title="Success", message=f"{e}", icon="info")
            
    
    def toggle_dirty_reading(self):
        state = self.switch_var.get() == str(1)
        
        DirtyReadingController.set_transaction_level(state)
        print(f"Dirty Reading is {'enabled' if state else 'disabled'}.")
        
        record = DirtyReadingController.fetch_by_table_name("repair")
        
        if record:
            if record[0].session_id != str(self.session_id):
                if state == True:
                    self.switch_var.set('0')
                else:
                    self.switch_var.set('1')
                self.switch.configure(state="disabled")
                CTkMessagebox(title="Error", message="You can not do that! Permitted only to the user, who turned it on / off.", icon="warning")
                
            else:
                if not state:
                    DirtyReadingController.delete("repair")
                else: 
                    DirtyReadingController.insert(DirtyReading("repair", session_id=self.session_id))        
        
        else:
            DirtyReadingController.insert(DirtyReading("repair", session_id=self.session_id))
            
    
    def get_dirty_reading_value(self, table_name):
        """
        Fetch the default value for the switch from the database based on table name.
        
        :param table_name: The name of the table to check.
        
        :return: "on" if a matching record exists, otherwise "off".
        """
        try:
            record = DirtyReadingController.fetch_by_table_name(table_name)

            if record:
                return '1'
            else:
                return '0'
        except Exception as e:
            print(f"Error fetching dirty reading value: {e}")
            return '0'
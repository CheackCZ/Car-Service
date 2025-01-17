from datetime import datetime

import customtkinter as ctk
from tkinter import ttk

from CTkMessagebox import CTkMessagebox

from src.models.repair_type import RepairType
from src.models.employee import Employee
from src.models.car import Car
from src.models.repair import Repair, State

from src.controllers.repair_controller import RepairController

from public.Repairs.repair_dialog import RepairDialog
from public.Repairs.repair_selector import RepairSelector


class RepairsOptions(ctk.CTkFrame):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")

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
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self, text="Dirty Reading", variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.place(x=20, y=200)
        

    def open_add_repair_dialog(self):
        """
        Opens the dialog to add a new repair.
        """
        dialog = RepairDialog(self, on_submit_callback=self.handle_add_repair, mode="add")
        dialog.grab_set()
        dialog.lift()

    def handle_add_repair(self, repair_data):
        """
        Handles adding a new repair to the database.
        """
        print(repair_data)
        
        try:
            repair_type_text = repair_data["repair_type"]
            repair_type_id = int(repair_type_text.split("(")[1].split(")")[0])
            
            car_id = repair_data["car_id"]
            employee_id=repair_data["employee_id"]
            
            new_repair = Repair(
                repair_type=RepairType(id=repair_type_id),
                employee=Employee(id=employee_id),
                car=Car(id=car_id),
                date_started=datetime.strptime(repair_data["date_started"], "%Y-%m-%d"),
                date_finished=datetime.strptime(repair_data["date_ended"], "%Y-%m-%d"),
                price=repair_data["price"],
                state=State(repair_data["state"])                
            )
            RepairController.insert(new_repair)
            CTkMessagebox(title="Success", message="Repair added successfully.", icon="info")
        except Exception as e:
            print(e)
            CTkMessagebox(title="Error", message=f"Failed to add repair: {e}", icon="warning")
            

    def open_repair_selector_for_edit(self):
        """
        Opens the repair selector to choose a repair for editing.
        """
        selector = RepairSelector(parent=self, on_submit_callback=self.open_edit_repair_dialog, title="Edit Repair", button_text="Edit Repair")
        selector.grab_set()
        selector.lift()
        

    def open_edit_repair_dialog(self, repair_id):
        """
        Opens the dialog to edit a selected repair.
        """
        try:
            repair = RepairController.fetch_by_id(repair_id)
            if not repair:
                CTkMessagebox(title="Error", message="Repair not found.", icon="warning")
                return

            repair_data = repair.to_dict()
            dialog = RepairDialog(self, on_submit_callback=self.handle_edit_repair, mode="edit", repair_data=repair_data)
            dialog.grab_set()
            dialog.lift()
            
        except Exception as e:
            print(f"Failed to fetch repair: {e}")

    def handle_edit_repair(self, repair_data):
        """
        Handles editing an existing repair in the database.
        """
        try:
            repair_type=repair_data["repair_type"]
            car_id = repair_data["car_id"]
            employee_id=repair_data["employee_id"]
            
            updated_repair = Repair(
                id=repair_data["id"],
                repair_type=RepairType(name=repair_type),
                employee=Employee(id=employee_id),
                car=Car(id=car_id),
                date_started=datetime.strptime(repair_data["date_started"], "%Y-%m-%d"),
                date_finished=datetime.strptime(repair_data["date_ended"], "%Y-%m-%d"),
                price=repair_data["price"],
                state=repair_data["state"]                
            )
            RepairController.update(updated_repair)
            CTkMessagebox(title="Success", message="Repair updated successfully.", icon="info")
        except Exception as e:
            print(e)
            CTkMessagebox(title="Error", message=f"Failed to edit repair: {e}", icon="warning")


    def open_repair_selector_for_remove(self):
        """
        Opens the repair selector to choose a repair for removal.
        """
        selector = RepairSelector(parent=self, on_submit_callback=self.handle_remove_repair, title="Remove Repair", button_text="Remove Repair")
        selector.grab_set()
        selector.lift()

    def handle_remove_repair(self, repair_id):
        """
        Handles removing a repair from the database.
        """
        try:
            RepairController.delete(repair_id)
            CTkMessagebox(title="Success", message="Repair deleted successfully.", icon="info")
        except Exception as e:
            CTkMessagebox(title="Success", message="Failed to delete repair.", icon="info")
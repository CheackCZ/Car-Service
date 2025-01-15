import customtkinter as ctk
from tkinter import ttk

from public.Employees.employee_dialog import EmployeeDialog

class EmployeesOptions(ctk.CTkFrame):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Label with "Tables" 
        self.db_name_label = ctk.CTkLabel(self, text="Options:", font=("Poppins", 14), text_color="gray", wraplength=160, justify="left")
        self.db_name_label.place(x=10, y=10)

        # Add Button
        self.add_button = ctk.CTkButton(self, command=self.open_add_employee_dialog, text="Add Employee", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.add_button.place(x=10, y=50)

        # Edit Button
        self.edit_button = ctk.CTkButton(self, command=self.open_edit_employee_dialog, text="Edit Employee", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.edit_button.place(x=10, y=90)

        # Remove Button
        self.remove_button = ctk.CTkButton(self, text="Remove Employee", border_width=2, border_color="#FF474D", hover_color="red", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.remove_button.place(x=10, y=130)

        # Separator
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.place(x=10, y=180, width=140)

        # Toggle Switch for Dirty Reading
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self, text="Dirty Reading", variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.place(x=20, y=200)
        

    def open_add_employee_dialog(self):
        dialog = EmployeeDialog(self, on_submit_callback=self.handle_add_employee, mode="add")
        dialog.lift()
        dialog.grab_set()

    def open_edit_employee_dialog(self):
        employee_data = {
            "first_name": "John",
            "middle_name": "Doe",
            "last_name": "Smith",
            "phone": "+123456789",
            "email": "john.smith@example.com",
        }
        dialog = EmployeeDialog(self, on_submit_callback=self.handle_edit_employee, mode="edit", employee_data=employee_data)
        dialog.lift()
        dialog.grab_set()

        
    def handle_add_employee():
        pass
    
    def handle_edit_employee(self):
        pass
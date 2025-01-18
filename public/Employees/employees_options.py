import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from tkinter import ttk

from public.Employees.employee_dialog import EmployeeDialog
from public.Employees.employee_selector import EmployeeSelector

from src.models.employee import Employee
from src.controllers.employee_controller import EmployeeController

class EmployeesOptions(ctk.CTkFrame):
    """ 
    A frame providing options for managing employees, such as adding, editing, and removing employees.
    """
    
    def __init__(self, parent, **kwargs):
        """
        Initialize the EmployeesOptions frame.
        
        :param parent: The parent widget.
        :param **kwargs: Additional keyword arguments for the frame configuration.
        """
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        # Label with "Tables" 
        self.db_name_label = ctk.CTkLabel(self, text="Options:", font=("Poppins", 14), text_color="gray", wraplength=160, justify="left")
        self.db_name_label.place(x=10, y=10)

        # Add Button
        self.add_button = ctk.CTkButton(self, command=self.open_add_employee_dialog, text="Add Employee", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.add_button.place(x=10, y=50)

        # Edit Button
        self.edit_button = ctk.CTkButton(self, command=self.open_employee_selector_for_edit, text="Edit Employee", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.edit_button.place(x=10, y=90)

        # Remove Button
        self.remove_button = ctk.CTkButton(self, command=self.open_employee_selector_for_delete, text="Remove Employee", border_width=2, border_color="#FF474D", hover_color="red", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.remove_button.place(x=10, y=130)
        
        # Separator
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.place(x=10, y=180, width=140)

        # Toggle Switch for Dirty Reading
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self, text="Dirty Reading", variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.place(x=20, y=200)
        

    def open_add_employee_dialog(self):
        """
        Opens the dialog to add a new employee.
        """
        dialog = EmployeeDialog(self, on_submit_callback=self.handle_add_employee, mode="add")
        dialog.grab_set()
        dialog.lift()
        
        
    def handle_add_employee(self, employee_data):
        """
        Handles adding an Employee with partial data.
        
        :param employee_data (dict): Data for the new employee.
        """
        try:
            new_employee = Employee(
                name=employee_data["name"],
                middle_name=employee_data.get("middle_name", ""),
                last_name=employee_data["last_name"],
                phone=employee_data.get("phone", ""),
                email=employee_data.get("email", ""),
                is_free=True  
            )

            EmployeeController.insert(new_employee)
            CTkMessagebox(title="Success", message="Employee added successfully.", icon="info")
        except ValueError as ve:
            CTkMessagebox(title="Validation Error", message=str(ve), icon="warning")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to add employee: {e}", icon="warning")


    
    def open_employee_selector_for_edit(self):
        """
        Opens the employee selector to choose an employee for editing.
        """
        selector = EmployeeSelector(
            parent=self,
            on_submit_callback=self.open_edit_employee_dialog,
            title="Edit Employee",
            button_text="Edit Employee"
        )
        selector.grab_set()
        selector.lift()

    def open_edit_employee_dialog(self, employee_id):
        """
        Opens the edit dialog for the selected employee.
        
        :param employee_id (int): ID of the employee to edit.
        """
        employee = EmployeeController.fetch_by_id(employee_id)
        
        if not employee:
            CTkMessagebox(title="Error", message="Employee not found.", icon="warning")
            return

        employee_data = employee.to_dict()
        employee_data["id"] = employee.id

        dialog = EmployeeDialog(
            self,
            on_submit_callback=self.handle_edit_employee,
            mode="edit",
            employee_data=employee_data
        )
        dialog.grab_set()
        dialog.lift()


    def handle_edit_employee(self, updated_data):
        """
        Handles the submission of updated employee data.
        
        :param updated_data (dict): Updated data for the employee.
        """
        print("Updated Data in handle_edit_employee:", updated_data)
         
        try:
            updated_employee = Employee(
                id=updated_data["id"],  # Explicitly set the ID
                name=updated_data.get("name", ""),
                middle_name=updated_data.get("middle_name", ""),
                last_name=updated_data.get("last_name", ""),
                phone=updated_data.get("phone", ""),
                email=updated_data.get("email", ""),
                is_free=updated_data.get("is_free", True),
            )

            EmployeeController.update(updated_employee)
            CTkMessagebox(title="Success", message="Employee updated successfully.", icon="info")
        except ValueError as ve:
            CTkMessagebox(title="Error", message=f"{ve}", icon="warning")    
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to update employee: {e}", icon="warning")


    def open_employee_selector_for_delete(self):
        """
        Opens the employee selector to choose an employee for deletion.
        """
        selector = EmployeeSelector(
            parent=self,
            on_submit_callback=self.confirm_delete_employee,
            title="Remove Employee",
            button_text="Remove Employee"
        )
        selector.grab_set()
        selector.lift()

    def confirm_delete_employee(self, employee_id):
        """
        Confirms and deletes the selected employee.
        
        :param employee_id (int): ID of the employee to delete.
        """
        confirm = CTkMessagebox(
            title="Confirm Deletion",
            message="Are you sure you want to delete this employee?",
            icon="question",
            options=["Yes", "No"],
        )
        if confirm.get() == "Yes":
            try:
                EmployeeController.delete(employee_id)
                CTkMessagebox(title="Success", message="Employee deleted successfully.", icon="info")
            except Exception as e:
                CTkMessagebox(title="Error", message=f"{e}", icon="warning")
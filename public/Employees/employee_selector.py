import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from src.controllers.employee_controller import EmployeeController

class EmployeeSelector(ctk.CTkToplevel):
    """
    A class for displaying a dropdown (combobox) of employees with their IDs.
    """
    
    def __init__(self, parent, on_submit_callback, title="Choose Employee", button_text="Submit",**kwargs):
        """
        Initialize the EmployeeSelector window.
        
        :param parent: Parent widget.
        :param on_selection_change: Callback function to handle changes in selection.
        :param kwargs: Additional arguments for the CTkFrame.
        """
        super().__init__(parent, **kwargs)

        self.employee_data = {}
        self.selected_employee_id = None
        self.on_submit_callback = on_submit_callback
        
        # Credentials
        self.title(title)
        self.geometry("260x180")
        self.resizable(False, False)
        
        self.parent = parent
        self.on_submit_callback = on_submit_callback
        
        # Label for employee selection
        self.label = ctk.CTkLabel(self, text="Employee Selection", text_color="white", font=("Poppins", 16, "bold"))
        self.label.place(relx = 0.5, y = 30, anchor="center")

        # ComboBox for employee selection
        self.combobox = ctk.CTkComboBox(self, width=200, values=[])
        self.combobox.place(relx = 0.5, y = 70, anchor="center")
        
        # Button for either removal / edit
        self.submit_button = ctk.CTkButton(self, text=button_text, command=self.submit_selection)
        self.submit_button.place(relx = 0.5, y = 130, anchor="center")
        
        self.load_employees()
    
    def load_employees(self):
        """
        Load employees from the database and populate the combobox.
        """
        try:
            employees = EmployeeController.fetch_all()
            
            self.employee_data = {
                f"({employee.id}) {employee.name} {employee.middle_name} {employee.last_name}": employee.id
                for employee in employees
            }
            
            self.combobox.configure(values=list(self.employee_data.keys()))
            
            self.combobox.set("")
            
        except Exception as e:
            print(f"Error loading employees: {e}")

    
    def submit_selection(self):
        """
        Handle the submission of the selected employee.
        """
        selected_text = self.combobox.get()
        self.selected_employee_id = self.employee_data.get(selected_text)
        if self.selected_employee_id:
            self.on_submit_callback(self.selected_employee_id)
            self.destroy()
        else:
            CTkMessagebox(title="Error", message="No employee selected.", icon="warning")
import customtkinter as ctk

from src.controllers.employee_controller import EmployeeController

class EmployeeSelector(ctk.CTkToplevel):
    
    def __init__(self, parent, on_submit_callback, **kwargs):
        """
        A class for displaying a dropdown (combobox) of employees with their IDs.
        
        :param parent: Parent widget.
        :param on_selection_change: Callback function to handle changes in selection.
        :param kwargs: Additional arguments for the CTkFrame.
        """
        super().__init__(parent, **kwargs)

        self.employee_data = {}
        self.selected_employee_id = None
        
        # Credentials
        title_text = "Choose Employee"
        self.title(title_text)
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
        self.submit_button = ctk.CTkButton(self, text=title_text, command=self.submit_selection)
        self.submit_button.place(relx = 0.5, y = 130, anchor="center")
        
        self.load_employees()
    
    def load_employees(self):
        """
        Load employees from the database and populate the combobox.
        """
        try:
            # Fetch all employees using EmployeeController
            employees = EmployeeController.fetch_all()
            
            # Create a mapping of display names to employee IDs
            self.employee_data = {
                f"({employee.id}) {employee.name} {employee.middle_name} {employee.last_name}": employee.id
                for employee in employees
            }
            
            # Populate the combobox with employee names
            self.combobox.configure(values=list(self.employee_data.keys()))
            
            # Set default value to an empty string (None equivalent)
            self.combobox.set("")
            
        except Exception as e:
            print(f"Error loading employees: {e}")

    
    def submit_selection(self):
        pass
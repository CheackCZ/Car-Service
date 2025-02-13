import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class EmployeeDialog(ctk.CTkToplevel):
    """
    A dialog window for adding or editing employee details. 
    The form includes fields for first name, middle name, last name, phone number, and email address, with options to submit the data.
    """
    
    def __init__(self, parent, on_submit_callback, mode="add", employee_data=None, **kwargs):
        """
        Initialize the EmployeeDialog.

        :param parent (ctk.CTk): The parent widget.
        :param on_submit_callback (callable): A function to handle form submission.
        :param mode (str): The mode of the dialog ("add" or "edit"). Default is "add".
        :param employee_data (dict, optional): The data for the employee being edited. Default is None.
        :param kwargs: Additional keyword arguments for the CTkToplevel.
        """
        super().__init__(**kwargs)

        self.mode = mode
        self.employee_data = employee_data if employee_data else {}

        # Credentials
        title_text = "Add Employee" if self.mode == "add" else "Edit Employee"  
        self.title(title_text)
        self.geometry("420x240")
        self.resizable(False, False)

        self.parent = parent
        self.on_submit_callback = on_submit_callback


        # Label with "Tables" 
        self.add_employee_label = ctk.CTkLabel(self, text=title_text, font=("Poppins", 16, "bold"), text_color="white", wraplength=160)
        self.add_employee_label.place(relx=0.5, y=30, anchor="center") 

        # First Name
        self.name_entry = ctk.CTkEntry(self, width=120, placeholder_text="First name")
        self.name_entry.place(x = 20, y = 70)
        self.fill_entry(self.name_entry, "name")

        # Middle Name
        self.middle_name_entry = ctk.CTkEntry(self, width=120, placeholder_text="Middle name")
        self.middle_name_entry.place(x = 150, y = 70)
        self.fill_entry(self.middle_name_entry, "middle_name") 

        # Last Name
        self.last_name_entry = ctk.CTkEntry(self, width=120, placeholder_text="Last name")
        self.last_name_entry.place(x = 280, y = 70)
        self.fill_entry(self.last_name_entry, "last_name")

        # Phone
        self.phone_entry = ctk.CTkEntry(self, width=185, placeholder_text="Phone number")
        self.phone_entry.place(x = 20, y = 120)
        self.fill_entry(self.phone_entry, "phone")

        # Email
        self.email_entry = ctk.CTkEntry(self, width=185, placeholder_text="Email address")
        self.email_entry.place(x = 215, y = 120)
        self.fill_entry(self.email_entry, "email")

        # Submit Button
        self.submit_button = ctk.CTkButton(self, text=title_text, command=self.submit_form)
        self.submit_button.place(relx = 0.5, y = 200, anchor="center")


    def submit_form(self):
        """
        Collects data from the form and invokes the callback to handle submission.
        """
        try:
            employee_data = {
                "id" : self.employee_data.get("id"),
                "name": self.name_entry.get(),
                "middle_name": self.middle_name_entry.get(),
                "last_name": self.last_name_entry.get(),
                "phone": self.phone_entry.get(),
                "email": self.email_entry.get(),
            }

            self.on_submit_callback(employee_data)

        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="warning")
            return

        self.destroy()
    
    
    def fill_entry(self, entry_widget, data_key):
        """
        Fills an entry widget with data from employee_data if in edit mode.
        
        :param entry_widget (ctk.CTkEntry): The entry widget to populate.
        :param data_key (str): The key to retrieve the corresponding value from employee_data.
        """
        if self.mode == "edit":
            entry_widget.insert(0, self.employee_data.get(data_key, ""))
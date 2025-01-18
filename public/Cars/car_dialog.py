from datetime import datetime

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from tkinter import ttk

from src.controllers.client_controller import ClientController
from src.controllers.brand_controller import BrandController

class CarDialog(ctk.CTkToplevel):
    """
    A dialog window for adding or editing car details. 
    The form includes fields for the client, brand, registration number, registration date, and model, with options to submit the data.
    """
    
    def __init__(self, parent, on_submit_callback, mode="add", car_data=None, **kwargs):
        """
        Initialize the CarDialog. 
    
        :param parent (ctk.CTk): The parent widget.
        :param on_submit_callback (callable): A function to handle form submission.
        :param mode (str): The mode of the dialog ("add" or "edit"). Default is "add".
        :param car_data (dict, optional): The data for the car being edited. Default is None.
        :param kwargs: Additional keyword arguments for the CTkToplevel.
        """    
        super().__init__(**kwargs)

        self.mode = mode
        self.car_data = car_data if car_data else {}

        # Set title and window properties
        title_text = "Add Car" if self.mode == "add" else "Edit Car"
        self.title(title_text)
        self.geometry("360x340")
        self.resizable(False, False)

        self.parent = parent
        self.on_submit_callback = on_submit_callback

        # Title Label
        self.title_label = ctk.CTkLabel(self, text=title_text, font=("Poppins", 16, "bold"), text_color="white")
        self.title_label.place(relx=0.5, y=30, anchor="center")

        # Combobox for Client
        self.client_label = ctk.CTkLabel(self, text="Client:", font=("Poppins", 12, "bold"))
        self.client_label.place(x=20, y=70)
        self.client_combobox = ttk.Combobox(self, values=[])
        self.client_combobox.place(x=150, y=70, width=190)

        # Combobox for Brand
        self.brand_label = ctk.CTkLabel(self, text="Brand:", font=("Poppins", 12, "bold"))
        self.brand_label.place(x=20, y=100)
        self.brand_combobox = ttk.Combobox(self, values=[])
        self.brand_combobox.place(x=150, y=100, width=190)

        # Entry for Registration number
        self.registration_number_label = ctk.CTkLabel(self, text="Registration number:", font=("Poppins", 12, "bold"))
        self.registration_number_label.place(x=20, y=150)
        self.registration_number_entry = ctk.CTkEntry(self, width=190)
        self.registration_number_entry.place(x=150, y=150)

        # Entry for Registration date
        self.reigstration_date_label = ctk.CTkLabel(self, text="Registration date:", font=("Poppins", 12, "bold"))
        self.reigstration_date_label.place(x=20, y=190)
        self.reigstration_date_entry = ctk.CTkEntry(self, width=190, placeholder_text="YYYY-MM-DD")
        self.reigstration_date_entry.place(x=150, y=190)

        # Entry for Model
        self.model_label = ctk.CTkLabel(self, text="Model:", font=("Poppins", 12, "bold"))
        self.model_label.place(x=20, y=230)
        self.model_entry = ctk.CTkEntry(self, width=190)
        self.model_entry.place(x=150, y=230)

        # Submit Button
        self.submit_button = ctk.CTkButton(self, text=title_text, command=self.submit_form)
        self.submit_button.place(relx=0.5, y=300, anchor="center")

        self.load_comboboxes()
        self.fill_entry()


    def load_comboboxes(self):
        """
        Fetch clients and brands from the database and populate the comboboxes with them.
        """
        try:
            clients = ClientController.fetch_all()
            client_values = [f"({client.id}) {client.name} {client.middle_name} {client.last_name}" for client in clients]
            
            self.client_combobox.configure(values=client_values)

            brands = BrandController.fetch_all()
            brand_values = [f"({brand.id}) {brand.name}" for brand in brands]
            
            self.brand_combobox.configure(values=brand_values)
        except Exception as e:
            print(f"Error loading comboboxes: {e}")
            

    def submit_form(self):
        """
        Collects data from the form and invokes the callback to handle submission.
        """
        try:
            # Extract client ID
            client_text = self.client_combobox.get()
            if client_text:
                client_id = int(client_text.split("(")[1].split(")")[0])
            else:
                raise ValueError("Please select a valid client.")

            # Extract brand ID
            brand_text = self.brand_combobox.get()
            if brand_text:
                brand_id = int(brand_text.split("(")[1].split(")")[0])
            else:
                raise ValueError("Please select a valid brand.")

            # Collect remaining data
            registration_number = self.registration_number_entry.get().strip()
            registration_date = datetime.strptime(self.reigstration_date_entry.get().strip(), "%Y-%m-%d")
            model = self.model_entry.get().strip()

            if not registration_number or not model:
                raise ValueError("Please fill in all required fields.")

            # Build car data
            car_data = {
                "id": self.car_data.get("id", None),
                "client_id": client_id,
                "brand_id": brand_id,
                "registration_number": registration_number,
                "registration_date": registration_date,
                "model": model,
            }

            self.on_submit_callback(car_data)

        except Exception as e:
            CTkMessagebox(title="Error", message=str(e), icon="warning")
            return

        self.destroy()

    def fill_entry(self):
        """
        Fills an entry widget with data from car_data if in edit mode.
        """
        if self.mode == "edit":
            # Set the client combobox value
            client_id = f"({self.car_data.get('client_id')})"  
            for value in self.client_combobox.cget("values"):
                if value.startswith(client_id): 
                    self.client_combobox.set(value)
                    break

            # Set the brand combobox value
            brand_name = self.car_data.get('brand_name')
            if brand_name:
                for value in self.brand_combobox.cget("values"):
                    if brand_name in value:  
                        self.brand_combobox.set(value)
                        break
                    
            self.registration_number_entry.insert(0, self.car_data.get("registration_number", ""))
            self.reigstration_date_entry.insert(0, self.car_data.get("registration_date", ""))
            self.model_entry.insert(0, self.car_data.get("model", ""))
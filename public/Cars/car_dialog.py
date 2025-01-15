import customtkinter as ctk
from tkinter import ttk

class CarDialog(ctk.CTkToplevel):
    
    def __init__(self, parent, on_submit_callback, mode="add", car_data=None, **kwargs):
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
        self.client_combobox = ttk.Combobox(self, values=["Ondřej Faltin (1)", "Ondřej Faltin (1)", "Ondřej Faltin (1)", "Ondřej Faltin (1)"])
        self.client_combobox.place(x=150, y=70, width=190)
        self.fill_entry(self.client_combobox, "client")

        # Combobox for Brand
        self.brand_label = ctk.CTkLabel(self, text="Brand:", font=("Poppins", 12, "bold"))
        self.brand_label.place(x=20, y=100)
        self.brand_combobox = ttk.Combobox(
            self, values=["ŠKODA", "Mercedes", "BMW"]
        )
        self.brand_combobox.place(x=150, y=100, width=190)
        self.fill_entry(self.brand_combobox, "brand")

        # Entry for Registration number
        self.registration_number_label = ctk.CTkLabel(self, text="Registration number:", font=("Poppins", 12, "bold"))
        self.registration_number_label.place(x=20, y=150)
        self.registration_number_entry = ctk.CTkEntry(self, width=190)
        self.registration_number_entry.place(x=150, y=150)
        self.fill_entry(self.registration_number_entry, "registration_number")
        
        # Entry for Registration date
        self.reigstration_date_label = ctk.CTkLabel(self, text="Registration date:", font=("Poppins", 12, "bold"))
        self.reigstration_date_label.place(x=20, y=190)
        self.reigstration_date_entry = ctk.CTkEntry(self, width=190)
        self.reigstration_date_entry.place(x=150, y=190)
        self.fill_entry(self.reigstration_date_entry, "registration_date")
        
        # Entry for Model
        self.model_label = ctk.CTkLabel(self, text="Model:", font=("Poppins", 12, "bold"))
        self.model_label.place(x=20, y=230)
        self.model_entry = ctk.CTkEntry(self, width=190)
        self.model_entry.place(x=150, y=230)
        self.fill_entry(self.model_entry, "model")


        # Submit Button
        self.submit_button = ctk.CTkButton(self, text=title_text, command=self.submit_form)
        self.submit_button.place(relx=0.5, y=300, anchor="center")

    def submit_form(self):
        pass

    def fill_entry(self, widget, data_key):
        """Fills a widget with data if in edit mode."""
        if self.mode == "edit" and data_key in self.car_data:
            widget.insert(0, self.car_data.get(data_key, ""))

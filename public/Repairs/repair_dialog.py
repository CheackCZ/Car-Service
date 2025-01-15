import customtkinter as ctk
from tkinter import ttk

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
        self.repair_type_combobox = ttk.Combobox(self, values=["Engine", "Tires", "Bodywork", "Other"])
        self.repair_type_combobox.place(x=150, y=70, width=190)
        self.fill_entry(self.repair_type_combobox, "repair_type")

        # Combobox for Employee
        self.employee_label = ctk.CTkLabel(self, text="Employee:", font=("Poppins", 12, "bold"))
        self.employee_label.place(x=20, y=100)
        self.employee_combobox = ttk.Combobox(
            self, values=["John Doe (ID: 1)", "Jane Smith (ID: 2)", "Mike Johnson (ID: 3)"]
        )
        self.employee_combobox.place(x=150, y=100, width=190)
        self.fill_entry(self.employee_combobox, "employee")

        # Combobox for Car
        self.car_label = ctk.CTkLabel(self, text="Car:", font=("Poppins", 12, "bold"))
        self.car_label.place(x=20, y=130)
        self.car_combobox = ttk.Combobox(
            self, values=["Toyota Corolla (ID: 1)", "Honda Civic (ID: 2)", "Ford Focus (ID: 3)"]
        )
        self.car_combobox.place(x=150, y=130, width=190)
        self.fill_entry(self.car_combobox, "car")


        # Date Picker for Start Date
        self.date_started_label = ctk.CTkLabel(self, text="Start Date:", font=("Poppins", 12, "bold"))
        self.date_started_label.place(x=20, y=180)
        self.date_started_entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD", width=190)
        self.date_started_entry.place(x=150, y=180)
        self.fill_entry(self.date_started_entry, "date_started")

        # Date Picker for End Date
        self.date_ended_label = ctk.CTkLabel(self, text="End Date:", font=("Poppins", 12, "bold"))
        self.date_ended_label.place(x=20, y=220)
        self.date_ended_entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD", width=190)
        self.date_ended_entry.place(x=150, y=220)
        self.fill_entry(self.date_ended_entry, "date_ended")

        # Price Input
        self.price_label = ctk.CTkLabel(self, text="Price (CZK):", font=("Poppins", 12, "bold"))
        self.price_label.place(x=20, y=270)
        self.price_entry = ctk.CTkEntry(self, placeholder_text="0.00", width=190)
        self.price_entry.place(x=150, y=270)
        self.fill_entry(self.price_entry, "price")

        # Combobox for State
        self.state_label = ctk.CTkLabel(self, text="State:", font=("Poppins", 12, "bold"))
        self.state_label.place(x=20, y=320)
        self.state_combobox = ttk.Combobox(self, values=["Pending", "In Progress", "Completed"])
        self.state_combobox.place(x=150, y=320, width=190)
        self.fill_entry(self.state_combobox, "state")

        # Submit Button
        self.submit_button = ctk.CTkButton(self, text=title_text, command=self.submit_form)
        self.submit_button.place(relx=0.5, y=380, anchor="center")

    def submit_form(self):
        pass

    def fill_entry(self, widget, data_key):
        """Fills a widget with data if in edit mode."""
        if self.mode == "edit" and data_key in self.repair_data:
            widget.insert(0, self.repair_data.get(data_key, ""))

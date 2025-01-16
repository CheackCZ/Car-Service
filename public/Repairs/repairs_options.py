import customtkinter as ctk
from tkinter import ttk

from public.Repairs.repair_dialog import RepairDialog

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
        self.edit_button = ctk.CTkButton(self, command=self.open_edit_repair_dialog, text="Edit Repair", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.edit_button.place(x=10, y=90)

        # Remove Button
        self.remove_button = ctk.CTkButton(self, text="Remove Repair", border_width=2, border_color="#FF474D", hover_color="red", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.remove_button.place(x=10, y=130)

        # Separator
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.place(x=10, y=180, width=140)

        # Toggle Switch for Dirty Reading
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self, text="Dirty Reading", variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.place(x=20, y=200)
        

    def open_add_repair_dialog(self):
        dialog = RepairDialog(self, on_submit_callback=self.handle_add_reapir, mode="add")
        dialog.lift()
        dialog.grab_set()

    def open_edit_repair_dialog(self):
        repair_data = {
            "repair_type": "Engine",
            "employee": "John Doe (ID: 1)",
            "car": "Toyota Corolla (ID: 1)",
            "date_started": "2023-10-01",
            "date_ended": "2023-10-15",
            "price": "1200.50",
            "state": "Completed",
        }
        dialog = RepairDialog(self, on_submit_callback=self.handle_edit_repair, mode="edit", repair_data=repair_data)
        dialog.lift()
        dialog.grab_set()

        
    def handle_add_reapir():
        pass
    
    def handle_edit_repair(self):
        pass
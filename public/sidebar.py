import customtkinter as ctk
from tkinter import ttk

class Sidebar(ctk.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, width=180, height=480, **kwargs)

        # Label with database name
        self.db_name_label = ctk.CTkLabel(self, text="Service", font=("Poppins", 16, "bold"), text_color="white", wraplength=160, justify="left")
        self.db_name_label.place(x = 20, y = 20)

        # Add Button
        self.add_button = ctk.CTkButton(self, text="Add Employee", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.add_button.place(x=20, y=60)

        # Edit Button
        self.edit_button = ctk.CTkButton(self, text="Edit Employee", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.edit_button.place(x=20, y=100)

        # Remove Button
        self.remove_button = ctk.CTkButton(self, text="Remove Employee", border_width=2, border_color="#FF474D", hover_color="red", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.remove_button.place(x=20, y=140)

        # Separator
        self.separator1 = ttk.Separator(self, orient="horizontal")
        self.separator1.place(x=20, y=190, width=140)

        # Toggle Switch for Dirty Reading
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(self, text="Dirty Reading", variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.place(x=20, y=210)

        # Separator
        self.separator2 = ttk.Separator(self, orient="horizontal")
        self.separator2.place(x=20, y=250, width=140)

        # Import Button
        self.import_button = ctk.CTkButton(self, text="Import",  border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.import_button.place(x=20, y=270)

        # Export Button
        self.export_button = ctk.CTkButton(self, text="Export",  border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.export_button.place(x=20, y=310)
        
        # Exit Button
        self.exit_button = ctk.CTkButton(self, text="Exit", fg_color="red", text_color="white", hover_color="#FF474D", cursor="hand2", command=self.exit_application)
        self.exit_button.place(relx=0.5, rely=1.0, anchor="s", y=-20)
        
    def exit_application(self):
        self.master.destroy()
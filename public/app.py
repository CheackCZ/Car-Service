import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.abspath(os.path.join(current_dir, "..")))

import customtkinter as ctk
from src.connection import Connection

from dash import Dashboard

class Landing(ctk.CTk):
    
    # Set appearance and theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    def __init__(self):
        super().__init__()
        self.title("Car Service")
        self.geometry("480x200")
        self.resizable(False, False)
        
        self.label = ctk.CTkLabel(self, text="Car Service Database Management", font=("Poppins", 16, "bold"), text_color="white").place(relx=0.5, y=25, anchor="n")
        self.button = ctk.CTkButton(self, text="", width=140, font=("Poppins", 12))

    def test_connection(self):
        success, text = Connection.connect_to_database()

        status = ctk.CTkLabel(self, text=text, font=("Poppins", 12, "bold"), text_color="green", wraplength=400)
        if success:
            self.button_configuration("Continue", self.open_dashboard)
        else:
            status.configure(text_color="red")    
            self.button_configuration("Exit", self.destroy)
            
        status.place(relx=0.5, y=75, anchor="n")
        self.button.place(relx=0.5, y=120, anchor="n")


    def button_configuration(self, text, command):
        self.button.configure(text=text, command=command)
        
    def open_dashboard(self):
        self.destroy()  
        dashboard = Dashboard()
        dashboard.mainloop()

# Run the application
if __name__ == "__main__":
    app = Landing()
    app.after(500, app.test_connection)
    app.mainloop()
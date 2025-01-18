import customtkinter as ctk
from src.connection import Connection

from public.dash import Dashboard


class Landing(ctk.CTk):
    """
    Class that represents the landing page of the Car Service Database Management application. It initializes the GUI and handles database connection testing.
    """    
    
    # Set appearance and theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    def __init__(self):
        """
        Initialize the landing page window.
        """
        super().__init__()
        
        self.title("Car Service")
        self.geometry("480x200")
        self.resizable(False, False)
        
        self.label = ctk.CTkLabel(self, text="Car Service Database Management", font=("Poppins", 16, "bold"), text_color="white").place(relx=0.5, y=25, anchor="n")
        self.button = ctk.CTkButton(self, text="", width=140, font=("Poppins", 12))
        

    def test_connection(self):
        """
        Test the database connection and update the UI accordingly.
        """
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
        """
        Configure the main button with specified text and command.
        
        :param text (str): The text to display on the button.
        :param command (callable): The function to execute when the button is clicked.
        """
        self.button.configure(text=text, command=command)
        
    def open_dashboard(self):
        """
        Close the landing page and open the dashboard.
        """
        self.destroy()  
        dashboard = Dashboard()
        dashboard.mainloop()


if __name__ == "__main__":
    app = Landing()
    app.after(500, app.test_connection)
    app.mainloop()
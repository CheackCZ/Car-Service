import customtkinter as ctk

import uuid

from public.sidebar import Sidebar
from public.content import Content

class Dashboard(ctk.CTk):
    """
    Class representing the main dashboard window of the Car Service application.
    """
    
    # Set appearance and theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    def __init__(self):
        """
        Initialize the dashboard window.
        """
        super().__init__()  
        
        self.SESSION_ID = uuid.uuid4()
        
        # Creates a main window with title and geometry
        self.title("Car Service")
        self.geometry("1080x560")
        self.resizable(False, False)
        
        # Sidebar on the left with the tables menu 
        self.sidebar = Sidebar(master=self, session_id=self.SESSION_ID)
        self.sidebar.place(x = 0, y = 0)

        # Main content on the right side
        self.content = Content(master=self, session_id=self.SESSION_ID)
        self.content.place(x = 200, y = 20)
        


# Run the application
if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
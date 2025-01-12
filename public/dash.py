import customtkinter as ctk

from sidebar import Sidebar

class Dashboard(ctk.CTk):
    
    # Set appearance and theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    def __init__(self):
        super().__init__()  
        
        # Creates a main window with title and geometry
        self.title("Car Service")
        self.geometry("720x480")
        self.resizable(False, False)

        # Sidebar on the left with the menu
        self.sidebar = Sidebar(master=self)
        self.sidebar.place(x = 0, y = 0)

# Run the application
if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
import customtkinter as ctk
from tkinter import Menu

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

        # Menubar (at the top)
        menu = Menu(self)
        self.config(menu=menu)

        filemenu = Menu(self)
        filemenu.add_command(label='Import JSON')
        filemenu.add_command(label='Export')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.quit)

        helpmenu = Menu(menu)
        helpmenu.add_command(label='About')

        menu.add_cascade(label='File', menu=filemenu)
        menu.add_cascade(label='Help', menu=helpmenu)


# Run the application
if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
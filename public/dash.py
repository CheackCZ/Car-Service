import customtkinter as ctk
from tkinter import Menu

# Creates a main window (name Dashboard)
# Set appearance and theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Creates a main window with title and geometry
root = ctk.CTk()
root.title("Car Service")
root.geometry("720x480")
root.resizable(False, False)

# Menubar (at the top)
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
filemenu.add_command(label='Import JSON')
filemenu.add_command(label='Export')
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)

helpmenu = Menu(menu)
helpmenu.add_command(label='About')

menu.add_cascade(label='File', menu=filemenu)
menu.add_cascade(label='Help', menu=helpmenu)

# Runs the application
root.mainloop()
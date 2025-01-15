import customtkinter as ctk
from PIL import Image

class EmployeeCard(ctk.CTkFrame):
    
    def __init__(self, master, employee_fname, employee_mname, employee_lname, employee_phone, employee_email, **kwargs):
        super().__init__(master, width=640, height=80, **kwargs)
        
        # Employee credentials 
        self.employee_fname = employee_fname
        self.employee_mname = employee_mname
        self.employee_lname = employee_lname
        
        self.employee_phone = employee_phone
        self.employee_email = employee_email
        
        
        # Account icon
        self.employee_icon = ctk.CTkImage(light_image=Image.open("./public/img/account.png"), size=(40, 50))
        self.employee_icon_label = ctk.CTkLabel(self, image=self.employee_icon, text="")
        self.employee_icon_label.place(x = 10, y = 10)
        
        # Label with Employee full name
        self.employee_name_label = ctk.CTkLabel(self, text=employee_fname + " " + employee_mname + " " + employee_lname, font=("Poppins", 16, "bold"))
        self.employee_name_label.place(x = 60, y = 10)
        
        # Label with Employee's phone number
        self.employee_phone_label = ctk.CTkLabel(self, text=employee_phone, font=("Poppins", 12), height=10, text_color="gray")
        self.employee_phone_label.place(x = 60, y = 40)
        
        # Label with Employee's email
        self.employee_email_label = ctk.CTkLabel(self, text=employee_email, font=("Poppins", 12), height=10, text_color="gray")
        self.employee_email_label.place(x = 60, y = 55)
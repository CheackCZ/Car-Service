import customtkinter as ctk
from PIL import Image

class EmployeeCard(ctk.CTkFrame):
    """
    Class representing a UI component for displaying details about an employee.
    """
    
    def __init__(self, master, name, middle_name, last_name, phone, email, is_free, **kwargs):
        """
        Initialize the EmployeeCard.

        :param master (ctk.CTk): The parent widget for the card.
        :param name (str): The first name of the employee.
        :param middle_name (str): The middle name of the employee.
        :param last_name (str): The last name of the employee.
        :param phone (str): The phone number of the employee.
        :param email (str): The email address of the employee.
        :param is_free (bool): The availability status of the employee (True if free, False if working).
        :param kwargs: Additional keyword arguments for the CTkFrame.
        """
        super().__init__(master, width=640, height=90, **kwargs)
        
        # Employee credentials 
        self.name = name
        self.middle_name = middle_name
        self.last_name = last_name
        
        self.phone = self.format_czech_phone_number(phone)
        self.email = email
        self.is_free = is_free
        
        
        # Account icon
        self.employee_icon = ctk.CTkImage(light_image=Image.open("./public/img/account.png"), size=(40, 50))
        self.employee_icon_label = ctk.CTkLabel(self, image=self.employee_icon, text="")
        self.employee_icon_label.place(x = 10, y = 10)
        
        # Label with Employee full name
        self.employee_name_label = ctk.CTkLabel(self, text=self.name + " " + self.middle_name + " " + self.last_name, font=("Poppins", 16, "bold"))
        self.employee_name_label.place(x = 60, y = 10)
        
        # Label with Employee's phone number
        self.employee_phone_label = ctk.CTkLabel(self, text="Tel:       " + self.phone, font=("Poppins", 12), height=10, text_color="gray")
        self.employee_phone_label.place(x = 60, y = 40)
        
        # Label with Employee's email
        self.employee_email_label = ctk.CTkLabel(self, text="Email:  " + self.email, font=("Poppins", 12), height=10, text_color="gray")
        self.employee_email_label.place(x = 60, y = 60)
        
        # Label with status of the Employee
        status_text = "Free" if self.is_free else "Working"
        status_color = "green" if self.is_free else "red"
        self.status = ctk.CTkLabel(self, text=status_text, font=("Poppins", 16, "bold"), height=10, text_color=status_color)
        self.status.place(relx=1, x = -20, rely = 0, y = 20, anchor="e")
    
        
    def format_czech_phone_number(self, phone):
        """
        Formats a Czech phone number to more readable form.
        
        :param phone (str): The phone number.
        
        :return: Formatted phone number.
        """
        phone = phone.replace(" ", "")  
        
        if phone.startswith("+420"):
            prefix = "+420"
            number = phone[4:] 
            
        elif phone.startswith("420"):
            prefix = "420"
            number = phone[3:]
        
        else:
            prefix = ""
            number = phone

        formatted_number = " ".join([number[i:i+3] for i in range(0, len(number), 3)])

        return f"{prefix} {formatted_number}".strip()
import customtkinter as ctk
from PIL import Image

class EmployeeCard(ctk.CTkFrame):
    
    def __init__(self, master, name, middle_name, last_name, phone, email, **kwargs):
        super().__init__(master, width=640, height=90, **kwargs)
        
        # Employee credentials 
        self.name = name
        self.middle_name = middle_name
        self.last_name = last_name
        
        self.phone = self.format_czech_phone_number(phone)
        self.email = email
        
        
        # Account icon
        self.employee_icon = ctk.CTkImage(light_image=Image.open("./public/img/account.png"), size=(40, 50))
        self.employee_icon_label = ctk.CTkLabel(self, image=self.employee_icon, text="")
        self.employee_icon_label.place(x = 10, y = 10)
        
        # Label with Employee full name
        self.employee_name_label = ctk.CTkLabel(self, text=self.name + " " + self.middle_name + " " + self.last_name, font=("Poppins", 16, "bold"))
        self.employee_name_label.place(x = 60, y = 10)
        
        # Label with Employee's phone number
        self.employee_phone_label = ctk.CTkLabel(self, text="Tel:      " + self.phone, font=("Poppins", 12), height=10, text_color="gray")
        self.employee_phone_label.place(x = 60, y = 40)
        
        # Label with Employee's email
        self.employee_email_label = ctk.CTkLabel(self, text="Email:  " + self.email, font=("Poppins", 12), height=10, text_color="gray")
        self.employee_email_label.place(x = 60, y = 60)
        
    
    def format_czech_phone_number(self, phone):
        """
        Formats a Czech phone number to more readable form.
        
        :param phone: The phone number string.
        :return: Formatted phone number string.
        """
        phone = phone.replace(" ", "")  # Remove any existing spaces
        
        # Check for and handle the +420 or 420 prefix
        if phone.startswith("+420"):
            prefix = "+420"
            number = phone[4:]  # Remove the prefix
        elif phone.startswith("420"):
            prefix = "420"
            number = phone[3:]  # Remove the prefix
        else:
            prefix = ""
            number = phone  # No prefix

        # Format the remaining number in groups of three
        formatted_number = " ".join([number[i:i+3] for i in range(0, len(number), 3)])

        # Combine prefix and formatted number
        return f"{prefix} {formatted_number}".strip()


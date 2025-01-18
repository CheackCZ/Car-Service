import customtkinter as ctk

from PIL import Image

class CarCard(ctk.CTkFrame):
    """
    Class representing a UI component for displaying details about a car.
    """
    
    def __init__(self, master, id, brand_name, model, registration_number, registration_date, client_name, client_last_name, client_id, **kwargs):
        """
        Initialize the CarCard.
        
        :param master (ctk.CTk): The parent widget for the card.
        :param id (int): The unique identifier of the car.
        :param brand_name (str): The brand of the car.
        :param model (str): The model of the car.
        :param registration_number (str): The car's registration number.
        :param registration_date (str): The date of the car's registration.
        :param client_name (str): The first name of the client associated with the car.
        :param client_last_name (str): The last name of the client associated with the car.
        :param client_id (int): The unique identifier of the client.
        :param kwargs: Additional keyword arguments for the CTkFrame.        
        """
        super().__init__(master, width=640, height=110, **kwargs)
        
        # Employee credentials 
        self.id = id
        self.brand_name = brand_name
        self.model = model
        self.registration_number = self.format_registration_number(registration_number)
        self.registration_date = registration_date
        self.client_name = client_name
        self.client_last_name = client_last_name
        self.client_id = client_id
        
        # Car icon
        self.car_icon = ctk.CTkImage(light_image=Image.open("./public/img/car.png"), size=(40, 50))
        self.car_icon_label = ctk.CTkLabel(self, image=self.car_icon, text="")
        self.car_icon_label.place(x = 10, y = 10)
        
        # Label with Car's brand and model
        self.car_data_label = ctk.CTkLabel(self, text=self.brand_name + " " + self.model + " (" + str(self.id) + ")", font=("Poppins", 16, "bold"))
        self.car_data_label.place(x = 60, y = 10) 
    
        # Label with Car's registration number
        self.car_registration_number_label = ctk.CTkLabel(self, text="SPZ:               " + self.registration_number, font=("Poppins", 12), height=10, text_color="gray")
        self.car_registration_number_label.place(x = 60, y = 40)
        
        # Label with Car's registration date
        self.car_registration_date_label = ctk.CTkLabel(self, text="Registered:  " + self.registration_date, font=("Poppins", 12), height=10, text_color="gray")
        self.car_registration_date_label.place(x = 60, y = 60)
        
        # Label with Client's name
        self.client_name_label = ctk.CTkLabel(self, text="Client:            " + self.client_name + " " + self.client_last_name + " (" + str(self.client_id) + ")", font=("Poppins", 12), height=10, text_color="gray")
        self.client_name_label.place(x = 60, y = 80)
        
        
    def format_registration_number(self, registration_number):
        """
        Formats a Czech registration number to specified form.
        
        :param registration_number (str): The raw registration number.
        
        :return: Formatted registration number.
        """
        if " " in registration_number and len(registration_number.split(" ")[-1]) == 4:
            return registration_number

        registration_number = registration_number.replace(" ", "").replace("-", "")

        if len(registration_number) > 4:
            return f"{registration_number[:-4]} {registration_number[-4:]}"
        
        return registration_number
import customtkinter as ctk

from PIL import Image

class RepairCard(ctk.CTkFrame):
    """
    Class representing a UI component for displaying details about a repair.
    """
    
    # Define state-to-color mapping
    STATE_COLORS = {
        "Pending": "gray",
        "In process": "yellow",
        "Completed": "green",
        "Canceled": "red"
    }
    
    def __init__(self, master, id, employee_name, employee_middle_name, employee_last_name, employee_id, car_model, car_registration_num, brand_name, repair_type, date_started, date_finished, price, state, **kwargs):
        """
        Initialize the RepairCard.
        
        :param master (ctk.CTk): The parent widget for the card.
        :param id (int): The unique identifier for the repair.
        :param employee_name (str): The name of the employee assigned to the repair.
        :param employee_id (int): The unique identifier of the employee.
        :param car_model (str): The model of the car being repaired.
        :param car_registration_num (str): The registration number of the car.
        :param brand_name (str): The brand of the car being repaired.
        :param repair_type (str): The type of the repair.
        :param date_started (str): The start date of the repair.
        :param date_finished (str): The end date of the repair.
        :param price (float): The cost of the repair.
        :param state (str): The current state of the repair (e.g., "Pending", "Completed").
        :param kwargs: Additional keyword arguments for the CTkFrame.
        """
        super().__init__(master, width=640, height=115, **kwargs)
        
        print(state)
        
        # Employee credentials 
        self.id = id
        
        self.car_registration_num = car_registration_num
        self.car_model = car_model
        
        self.brand_name = brand_name
        
        self.employee_name = employee_name
        self.employee_middle_name = employee_middle_name
        self.employee_last_name = employee_last_name
        self.employee_id = employee_id 
        
        self.repair_type = repair_type
        
        self.date_started = date_started
        self.date_finished = date_finished
        self.price = price
        self.state = state
        
        
        # Repair icon
        self.repair_icon = ctk.CTkImage(light_image=Image.open("./public/img/repair.png"), size=(40, 50))
        self.repair_icon_label = ctk.CTkLabel(self, image=self.repair_icon, text="")
        self.repair_icon_label.place(x = 10, y = 10)
        
        # Label with Repair's ID
        self.repair_data_label = ctk.CTkLabel(self, text=repair_type + " (" + str(self.id) + ")", font=("Poppins", 16, "bold"))
        self.repair_data_label.place(x = 60, y = 10)
    
        # Date Started
        self.date_started_label = ctk.CTkLabel(self, text="From: " + date_started, font=("Poppins", 12), height=10, text_color="gray")
        self.date_started_label.place(x = 60, y = 40)
        
        # Date Finished
        self.date_finished_label = ctk.CTkLabel(self, text="To:      " + date_finished, font=("Poppins", 12), height=10, text_color="gray")
        self.date_finished_label.place(x = 60, y = 55)
        
        # Label with Car's model and registration number
        self.car_data_label = ctk.CTkLabel(self, text="Car:    " + brand_name + " " + car_model + " (" + car_registration_num + ")", font=("Poppins", 12), height=10, text_color="gray")
        self.car_data_label.place(x = 60, y = 75)
        
        # Label with Employee's name and id
        if self.employee_middle_name == None:
            self.employee_data_label = ctk.CTkLabel(self, text=f"Empl: {self.employee_name} {self.employee_last_name} (" + str(self.employee_id) + ")", font=("Poppins", 12), height=10, text_color="gray")
        else:
            self.employee_data_label = ctk.CTkLabel(self, text=f"Empl: {self.employee_name} {self.employee_middle_name} {self.employee_last_name} (" + str(self.employee_id) + ")", font=("Poppins", 12), height=10, text_color="gray")
        self.employee_data_label.place(x = 60, y = 90)
        
        # State with dynamic color
        state_color = self.STATE_COLORS.get(state, "gray")
        self.state_label = ctk.CTkLabel(self, text=state, font=("Poppins", 16, "bold"), height=10, text_color=state_color)
        self.state_label.place(relx=1, x = -20, rely = 0, y = 20, anchor="e")
        
        # Label with Repair's price
        self.price_label = ctk.CTkLabel(self, text=str(price) + " CZK", font=("Poppins", 12), height=10, text_color="gray")
        self.price_label.place(relx=1, x =- 20, rely = 0, y = 40, anchor="e")
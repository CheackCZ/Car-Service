import customtkinter as ctk
from PIL import Image

class RepairCard(ctk.CTkFrame):
    
    # Define state-to-color mapping
    STATE_COLORS = {
        "Pending": "gray",
        "In process": "yellow",
        "Completed": "green",
        "Canceled": "red"
    }
    
    def __init__(self, master, id, employee_name, employee_id, car_model, car_registration_num, brand_name, repair_type, date_started, date_finished, price, state, **kwargs):
        super().__init__(master, width=640, height=100, **kwargs)
        
        print(state)
        
        # Employee credentials 
        self.id = id
        self.car_registration_num = car_registration_num
        self.car_model = car_model
        self.brand_name = brand_name
        self.employee_name = employee_name
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
        
        
        # State with dynamic color
        state_color = self.STATE_COLORS.get(state, "gray")
        self.state_label = ctk.CTkLabel(self, text=state, font=("Poppins", 16, "bold"), height=10, text_color=state_color)
        self.state_label.place(relx=1, x = -20, rely = 0, y = 20, anchor="e")
        
        # Price
        if state == "Canceled":
            self.price_label = ctk.CTkLabel(self, text=str(price) + " CZK", font=("Poppins", 12), height=10, text_color="red")
        else:
            self.price_label = ctk.CTkLabel(self, text=str(price) + " CZK", font=("Poppins", 12), height=10, text_color="gray")

        self.price_label.place(relx=1, x =- 20, rely = 0, y = 40, anchor="e")
        
        
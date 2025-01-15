import customtkinter as ctk

from public.Cars.car_card import CarCard

class CarsFrame(ctk.CTkScrollableFrame):
    
     def __init__(self, master, **kwargs):
        super().__init__(master, width=650, height=450, **kwargs)
        
        # Content showing the values in the given table
        self.car1 = CarCard(self, 1, "ŠKODA", "Octavia", "5AS 9653", "14.1.2016", "Ondřej Faltin", 1, cursor="hand2")
        self.car1.pack(pady=5, padx=5, anchor="w")  
         
        # Content showing the values in the given table
        self.car2 = CarCard(self, 1, "ŠKODA", "Octavia", "5AS 9653", "14.1.2016", "Ondřej Faltin", 1, cursor="hand2")
        self.car2.pack(pady=5, padx=5, anchor="w")  
        
        # Content showing the values in the given table
        self.car3 = CarCard(self, 1, "ŠKODA", "Octavia", "5AS 9653", "14.1.2016", "Ondřej Faltin", 1, cursor="hand2")
        self.car3.pack(pady=5, padx=5, anchor="w")  
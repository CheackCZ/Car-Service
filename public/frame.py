import customtkinter as ctk

from .Cars.car_card import CarCard
from .Employees.employee_card import EmployeeCard
from .Repairs.repair_card import RepairCard


class Frame(ctk.CTkScrollableFrame):
   
      def __init__(self, master, **kwargs):
         super().__init__(master, width=650, height=450, **kwargs)

         self.card_classes = {
               "car": CarCard,
               "employee": EmployeeCard,
               "repair": RepairCard
         }

      def update_content(self, data, table_name):
         for widget in self.winfo_children():
            widget.destroy()
            
         print(table_name)

         card_class = self.card_classes.get(table_name)
         if not card_class:
               label = ctk.CTkLabel(self, text=f"No card class defined for {table_name}.", anchor="center")
               label.pack(expand=True, pady=10)
               return

         for record in data:
            try:
               card = card_class(self, **record.to_dict())
               card.pack(pady=5)
            except TypeError as e:
               print(e)
               label = ctk.CTkLabel(self, text=f"Error creating card: {e}", anchor="center", text_color="red")
               label.pack(expand=True, pady=10)
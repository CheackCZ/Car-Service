import customtkinter as ctk

from src.controllers.repair_controller import RepairController
from src.controllers.employee_controller import EmployeeController
from src.controllers.brand_controller import BrandController
from src.controllers.repair_type_controller import RepairTypeController
from src.controllers.car_controller import CarController
from src.controllers.client_controller import ClientController


class Tables(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=140, height=420, **kwargs)
        self.master = master 
        self.buttons = {}
        self.active_button = None

        # Adding buttons with dynamic show_data method
        self.add_table_button("repair", lambda: self.show_data(RepairController, "repair"))
        self.add_table_button("employee", lambda: self.show_data(EmployeeController, "employee"))
        self.add_table_button("car", lambda: self.show_data(CarController, "car"))
        self.add_table_button("client", lambda: self.show_data(ClientController, "client"))
        self.add_table_button("repair_ype", lambda: self.show_data(RepairTypeController, "repair_type"))
        self.add_table_button("brand", lambda: self.show_data(BrandController, "brand"))

        
        
    def add_table_button(self, text, command):
        button = ctk.CTkButton(self, text=text, fg_color="transparent", border_color="#3B8ED0", border_width=2, cursor="hand2", command=command)
        button.pack(pady=5)
        self.buttons[text] = button
   
    def update_content(self, data, table_name):
        self.master.master.content.frame.update_content(data, table_name)

    def show_data(self, controller, table_name):
        try:
            data = controller.fetch_all()
        except AttributeError:
            data = []
        self.update_content(data, table_name)
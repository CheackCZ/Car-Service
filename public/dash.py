import customtkinter as ctk

import uuid

from public.sidebar import Sidebar
from public.content import Content

from src.connection import Connection

from src.controllers.repair_controller import RepairController
from src.controllers.repair_type_controller import RepairTypeController
from src.controllers.brand_controller import BrandController
from src.controllers.car_controller import CarController
from src.controllers.client_controller import ClientController
from src.controllers.employee_controller import EmployeeController


class Dashboard(ctk.CTk):
    """
    Class representing the main dashboard window of the Car Service application.
    """
    
    # Set appearance and theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    def __init__(self):
        """
        Initialize the dashboard window.
        """
        super().__init__()  
        
        self.SESSION_ID = uuid.uuid4()
        
        self.conn = Connection.connection()
        
        # Create instances of controllers
        self.repair_controller = RepairController(self.conn)
        self.employee_controller = EmployeeController(self.conn)
        self.car_controller = CarController(self.conn)
        self.client_controller = ClientController(self.conn)
        self.repair_type_controller = RepairTypeController(self.conn)
        self.brand_controller = BrandController(self.conn)
        
        # Creates a main window with title and geometry
        self.title("Car Service")
        self.geometry("1080x560")
        self.resizable(False, False)
        
        # Sidebar on the left with the tables menu 
        self.sidebar = Sidebar(master=self, session_id=self.SESSION_ID, repair_controller=self.repair_controller, employee_controller=self.employee_controller, 
                               car_controller=self.car_controller, client_controller=self.client_controller, repair_type_controller=self.repair_type_controller, brand_controller=self.brand_controller)
        self.sidebar.place(x = 0, y = 0)

        # Main content on the right side
        self.content = Content(master=self, session_id=self.SESSION_ID, repair_controller=self.repair_controller, employee_controller=self.employee_controller, 
                               car_controller=self.car_controller, client_controller=self.client_controller, repair_type_controller=self.repair_type_controller, brand_controller=self.brand_controller)

        self.content.place(x = 200, y = 20)
        


# Run the application
if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
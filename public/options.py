import customtkinter as ctk

from public.Cars.car_options import CarsOptions
from public.Employees.employees_options import EmployeesOptions
from public.Repairs.repairs_options import RepairsOptions


class Options(ctk.CTkFrame):
    """
    Class with frame displaying table-specific options in the Car Service application.
    """
        
    def __init__(self, parent, session_id, repair_controller, repair_type_controller, employee_controller, car_controller, brand_controller, client_controller, **kwargs):
        """
        Initialize the Options frame.

        :param parent (ctk.CTk): The parent widget for the options frame.
        :param kwargs: Additional keyword arguments for the CTkFrame.
        """
        super().__init__(parent, **kwargs)
            
        self.session_id = session_id
        
        self.repair_controller = repair_controller
        self.employee_controller = employee_controller
        self.car_controller = car_controller
        self.brand_controller = brand_controller 
        self.client_controller= client_controller
        self.repair_type_controller = repair_type_controller
                
        # Mapping table names to their respective options class and controller
        self.options_mapping = {
            "car": (CarsOptions, self.car_controller),
            "employee": (EmployeesOptions, self.employee_controller),
            "repair": (RepairsOptions, self.repair_controller),
        }

        self.current_options = None 

    def show_options(self, table_name):
        """
        Switch to the options frame for the specified table.        
        
        :param table_name (str): The name of the active table whose options are to be displayed.
        """
        # Destroy the current options frame if it exists
        if self.current_options is not None:
            self.current_options.destroy()
            self.current_options = None

        # Fetch the options class and controller for the given table
        options_data = self.options_mapping.get(table_name)

        if options_data is not None:
            options_class, controller = options_data
            
            # If table is "car," include brand_controller
            if table_name == "car":
                self.current_options = options_class(
                    self, 
                    width=160, 
                    height=240, 
                    session_id=self.session_id, 
                    controller=controller, 
                    brand_controller=self.brand_controller,
                    client_controller=self.client_controller
                )
            elif table_name == "repair":
                self.current_options = options_class(
                    self, 
                    width=160, 
                    height=240, 
                    session_id=self.session_id, 
                    controller=controller, 
                    car_controller=self.car_controller,
                    employee_controller=self.employee_controller,
                    repair_type_controller=self.repair_type_controller
                )
            else:
                # Instantiate the options frame with the appropriate controller
                self.current_options = options_class(
                    self, 
                    width=160, 
                    height=240, 
                    session_id=self.session_id, 
                    controller=controller
                )
            
            self.current_options.place(x=0, y=0)
        else:
            # Display a fallback label if no options are defined for the table
            label = ctk.CTkLabel(self, text=f"No options frame defined for {table_name}.", wraplength=150, anchor="w")
            label.place(x=10, y=10)

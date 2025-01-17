import customtkinter as ctk

from .Cars.car_options import CarsOptions
from .Employees.employees_options import EmployeesOptions
from .Repairs.repairs_options import RepairsOptions

class Options(ctk.CTkFrame):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
            
        self.current_options = None 
        self.options_mapping = {
            "car": CarsOptions,
            "employee": EmployeesOptions,
            "repair": RepairsOptions,
        }

    def show_options(self, table_name):
        """Switches to the options frame for the given table."""
        if self.current_options is not None:
            self.current_options.destroy()
            self.current_options = None

        options_class = self.options_mapping.get(table_name)
        
        if options_class is not None:
            self.current_options = options_class(self, width=160, height=240)
            self.current_options.place(x=0, y=0)
        else:
            label = ctk.CTkLabel(self, text=f"No options frame defined for {table_name}.", wraplength=150, anchor="w")
            label.place(x = 10, y = 10)
            return
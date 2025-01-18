import customtkinter as ctk

from public.Cars.car_options import CarsOptions
from public.Employees.employees_options import EmployeesOptions
from public.Repairs.repairs_options import RepairsOptions


class Options(ctk.CTkFrame):
    """
    Class with frame displaying table-specific options in the Car Service application.
    """
        
    def __init__(self, parent, **kwargs):
        """
        Initialize the Options frame.

        :param parent (ctk.CTk): The parent widget for the options frame.
        :param kwargs: Additional keyword arguments for the CTkFrame.
        """
        super().__init__(parent, **kwargs)
            
        self.current_options = None 
        self.options_mapping = {
            "car": CarsOptions,
            "employee": EmployeesOptions,
            "repair": RepairsOptions,
        }


    def show_options(self, table_name):
        """
        Switch to the options frame for the specified table.        
        
        :param table_name (str): The name of the active table whose options are to be displayed.
        """
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
import customtkinter as ctk

from search import SearchBar
from public.import_and_export import ImportExport

from public.Employees.employees_options import EmployeesOptions
from public.Repairs.repairs_options import RepairsOptions
from public.Cars.car_options import CarsOptions

from public.Employees.employees_frame import EmployeesFrame
from public.Repairs.repairs_frame import RepairsFrame
from public.Cars.cars_frame import CarsFrame

class Content(ctk.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, width=860, height=520, **kwargs)

        # Frame with values from Employees table
        # self.employees_frame = EmployeesFrame(self)
        # self.employees_frame.place(x = 10, y = 10)
        
        # Frame with values from Repairs Table
        self.repairs_frame = RepairsFrame(self)
        self.repairs_frame.place(x = 10, y = 10)

        # Frame with values from Cars Table
        # self.cars_frame = CarsFrame(self)
        # self.cars_frame.place(x = 10, y = 10)
      

        # Options Employees Frame
        # self.employees_options_frame = EmployeesOptions(self, width=160, height=240)
        # self.employees_options_frame.place(x=690, y=10)
        
        # Options Repairs Frame
        # self.repairs_options_frame = RepairsOptions(self, width=160, height=240)
        # self.repairs_options_frame.place(x=690, y=10)
        
        # Options Cars Frame
        self.cars_options_frame = CarsOptions(self, width=160, height=240)
        self.cars_options_frame.place(x=690, y=10)
        
        
        # Import/Export frame
        self.import_export_frame = ImportExport(self, width=160, height=90)
        self.import_export_frame.place(x=690, y=260)
        
        # Searchbar to search for given value in (database) table 
        self.tables_search = SearchBar(self, on_search=None, placeholder_text="Search for a value...")
        self.tables_search.place(x = 0, y = 480)
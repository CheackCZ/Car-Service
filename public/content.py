import customtkinter as ctk

from public.search import SearchBar
from public.import_and_export import ImportExport
from public.options import Options
from public.frame import Frame


class Content(ctk.CTkFrame):
    """
    Class representing the main content area of the Car Service application.
    """
    
    def __init__(self, master, repair_controller, employee_controller, car_controller, client_controller, repair_type_controller, brand_controller, session_id, **kwargs):
        """
        Initialize the Content frame.
        
        :param master (ctk.CTk): The parent widget for the content frame.
        :param kwargs: Additional keyword arguments for the CTkFrame.
        """
        super().__init__(master, width=860, height=520, **kwargs)

        self.active_table = None
        self.all_data = []
        
        self.repair_controller = repair_controller
        self.employee_controller = employee_controller
        self.car_controller = car_controller
        self.client_controller = client_controller
        self.repair_type_controller = repair_type_controller
        self.brand_controller = brand_controller
        
        # Map table names to controller instances
        self.controller_map = {
            "repair": self.repair_controller,
            "employee": self.employee_controller,
            "car": self.car_controller,
            "client": self.client_controller,
            "repair_type": self.repair_type_controller,
            "brand": self.brand_controller,
        }


        # Frame with values from chosen Table
        self.frame = Frame(self)
        self.frame.place(x = 10, y = 10)

        # Options with button from chosen Table
        self.options = Options(self, session_id=session_id, repair_controller=self.repair_controller, employee_controller = self.employee_controller, car_controller=self.car_controller, brand_controller=self.brand_controller, client_controller=self.client_controller, width=160, height=240)
        self.options.place(x=690, y=10)
        
        # Import/Export frame
        self.import_export_frame = ImportExport(self, get_active_table_callback=self.get_active_table, repair_controller=self.repair_controller, employee_controller = self.employee_controller, car_controller=self.car_controller, width=160, height=90)
        self.import_export_frame.place(x=690, y=260)
        
        # Searchbar to search for given value in (database) table 
        self.tables_search = SearchBar(self, on_search=self.perform_search, placeholder_text="Search for a value...")
        self.tables_search.place(x = 0, y = 480)
    
    
    def update_options(self, table_name):
        """
        Update the options and import/export visibility based on the active table.
        
        :param table_name (str): The name of the active table.
        """
        self.active_table = table_name
        self.options.show_options(table_name)
        self.import_export_frame.update_visibility(table_name)
        
        # Fetch data for the active table and update the frame
        data = self.fetch_data_for_table(table_name)
        self.all_data = data 
        self.frame.update_content(data, table_name)

        
    def get_active_table(self):
        """
        Get the name of the currently active table.
        
        :return str: The name of the active table.
        """
        return self.active_table
    
    def fetch_data_for_table(self, table_name):
        """
        Fetch data from the corresponding controller instance based on the table name.
        
        :param table_name (str): The name of the table.
        :return list: Data fetched from the controller.
        """
        controller = self.controller_map.get(table_name)
        
        if controller:
            return controller.fetch_all()
        return []

    def perform_search(self, query):
        if not query:
            self.frame.update_content(self.all_data, self.active_table)
            return

        filtered_data = []
        if self.active_table == "employee":
            filtered_data = [
                item for item in self.all_data
                if any(
                    query.lower() in str(getattr(item, attr, "")).lower()
                    for attr in ["name", "middle_name", "last_name", "id"]
                )
            ]
        elif self.active_table == "car":
            filtered_data = [
                item for item in self.all_data
                if any(
                    query.lower() in str(getattr(item, attr, "")).lower()
                    for attr in ["brand", "model", "id"]
                )
            ]
        elif self.active_table == "repair":
            filtered_data = [
                item for item in self.all_data
                if any(
                    query.lower() in str(getattr(item, attr, "")).lower()
                    for attr in ["repair_type", "id"]
                )
            ]
        self.frame.update_content(filtered_data, self.active_table)

    def get_active_table(self):
        return self.active_table
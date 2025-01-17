import customtkinter as ctk

from .search import SearchBar
from .import_and_export import ImportExport

from .options import Options
from .frame import Frame
class Content(ctk.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, width=860, height=520, **kwargs)

        self.active_table = None

        # Frame with values from chosen Table
        self.frame = Frame(self)
        self.frame.place(x = 10, y = 10)

        # Options with button from chosen Table
        self.options = Options(self, width=160, height=240)
        self.options.place(x=690, y=10)
        
        # Import/Export frame
        self.import_export_frame = ImportExport(self, get_active_table_callback=self.get_active_table, width=160, height=90)
        self.import_export_frame.place(x=690, y=260)
        
        # Searchbar to search for given value in (database) table 
        self.tables_search = SearchBar(self, on_search=None, placeholder_text="Search for a value...")
        self.tables_search.place(x = 0, y = 480)
    
    
    def update_options(self, table_name):
        self.active_table = table_name
        self.options.show_options(table_name)
        self.import_export_frame.update_visibility(table_name)

        
    def get_active_table(self):
        return self.active_table
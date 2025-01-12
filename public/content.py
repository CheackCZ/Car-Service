import customtkinter as ctk

from tables import Tables
from table_view import TableView

class Content(ctk.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, width=740, height=440, **kwargs)

        # Table values view
        self.table_view = TableView(master=self)
        self.table_view.place(x=10, y=10)
        
        # Scrollable frame with all tables in given database
        self.tables_container = Tables(master=self)
        self.tables_container.place(x = 570, y = 10)
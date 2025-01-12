import customtkinter as ctk

class Tables(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        """
        Scrollable frame for listing tables with their associated buttons.
        """
        super().__init__(master, width=140, height=410, **kwargs)

        # Button for the table view
        self.table_button1 = ctk.CTkButton(self, text="Employee", fg_color="transparent", border_color="#3B8ED0", border_width=2, cursor="hand2")
        self.table_button1.pack(pady=5)

        # Another button for the table view
        self.table_button2 = ctk.CTkButton(self, text="Repair", fg_color="transparent", border_color="#3B8ED0", border_width=2, cursor="hand2")
        self.table_button2.pack(pady=5)
        
        # Another button for the table view
        self.table_button3 = ctk.CTkButton(self, text="Repair Type", fg_color="transparent", border_color="#3B8ED0", border_width=2, cursor="hand2")
        self.table_button3.pack(pady=5)
        
        # Another button for the table view
        self.table_button4 = ctk.CTkButton(self, text="Client", fg_color="transparent", border_color="#3B8ED0", border_width=2, cursor="hand2")
        self.table_button4.pack(pady=5)

        # Another button for the table view
        self.table_button5 = ctk.CTkButton(self, text="Car", fg_color="transparent", border_color="#3B8ED0", border_width=2, cursor="hand2")
        self.table_button5.pack(pady=5)
        
        # Another button for the table view
        self.table_button6 = ctk.CTkButton(self, text="Brand", fg_color="transparent", border_color="#3B8ED0", border_width=2, cursor="hand2")
        self.table_button6.pack(pady=5)

import customtkinter as ctk
from CTkTable import CTkTable

class TableView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=550, height=420, **kwargs)

        # Example table data
        value = [
            ["name", "middle_name", "last_name", "phone", "email"],
            ["Ondřej", "Martin", "Faltin", 774102991, "ondra.faltin@gmail.com"],
            ["Tomáš", "", "Kléger", 111222333, "thastertyn@thastertyn.xyz"],
            ["Adam", "", "Matys", 333222111, "matysek@pindysek.org"],
            ["Denis", "Kratom", "Heim", 123456789, "kratak@kratom.denis"],
        ]

        # Create CTkTable instance inside this frame
        self.table = CTkTable(
            master=self, 
            row=5, 
            column=5, 
            values=value, 
            fg_color="white", 
            text_color="white",
            wraplength=90,
            width=100,
            justify="left"
        )
        self.table.place(x=10, y=10)

import customtkinter as ctk

class Tables(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=140, height=420, **kwargs)

        self.buttons = {}
        self.active_button = None

        self.add_table_button("Repair", self.show_repairs)
        self.add_table_button("Employee", self.show_employees)
        self.add_table_button("Car", self.show_cars)
        self.add_table_button("Client", self.show_clients)
        self.add_table_button("Repair Type", self.show_repair_types)
        self.add_table_button("Brand", self.show_brands)
        

    def add_table_button(self, text, command):
        button = ctk.CTkButton(self, text=text, fg_color="transparent", border_color="#3B8ED0", border_width=2, cursor="hand2", command=lambda: self.update_content(command, button))
        button.pack(pady=5)
        self.buttons[text] = button

    def update_content(self, command, button):
        if self.active_button:
            self.active_button.configure(fg_color="transparent", text_color="white")

        button.configure(fg_color="#3B8ED0", text_color="white")
        self.active_button = button

        command()

    def show_repairs(self):
        print("repairs")

    def show_employees(self):
        print("employees")
        
    def show_cars(self):
        print("cars")

    def show_clients(self):
        print("clients")

    def show_repair_types(self):
        print("repair_types")

    def show_brands(self):
        print("brands")
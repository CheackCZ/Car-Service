import customtkinter as ctk

class Tables(ctk.CTkScrollableFrame):
    """
    Class representing a scrollable frame containing buttons to navigate and display data for different tables in the Car Service application.
    """
    
    def __init__(self, master, repair_controller, employee_controller, car_controller, client_controller, repair_type_controller, brand_controller, session_id, **kwargs):
        """
        Initialize the Tables frame.

        :param master (ctk.CTk): The parent widget for the frame.
        :param kwargs: Additional keyword arguments for the CTkScrollableFrame.    
        """
        super().__init__(master, width=140, height=390, **kwargs)
        
        self.master = master 
        
        self.buttons = {}
        self.active_button = None
        
        # Adding buttons with dynamic show_data method
        self.repair_controller = repair_controller
        self.employee_controller = employee_controller
        self.car_controller = car_controller
        self.client_controller = client_controller
        self.repair_type_controller = repair_type_controller
        self.brand_controller = brand_controller
        
        # Add table buttons with instance references
        self.add_table_button("repair", lambda: self.show_data(self.repair_controller, "repair"))
        self.add_table_button("employee", lambda: self.show_data(self.employee_controller, "employee"))
        self.add_table_button("car", lambda: self.show_data(self.car_controller, "car"))
        self.add_table_button("client", lambda: self.show_data(self.client_controller, "client"))
        self.add_table_button("repair_type", lambda: self.show_data(self.repair_type_controller, "repair_type"))
        self.add_table_button("brand", lambda: self.show_data(self.brand_controller, "brand"))
        
        
    def add_table_button(self, text, command):
        """
        Add a button to the frame for a specific table.
        
        :param text (str): The label for the button.
        :param command (callable): The function to execute when the button is clicked.
        """
        button = ctk.CTkButton(self, text=text, command=command, fg_color="transparent", border_color="#3B8ED0", border_width=2, cursor="hand2")
        button.pack(pady=5)
        self.buttons[text] = button
   
    def update_content(self, data, table_name):
        """
        Update the main content frame with the data from the selected table.

        :param data (list): The data to display in the main content frame.
        :param table_name (str): The name of the table whose data is being displayed.
        """
        self.master.master.content.frame.update_content(data, table_name)

    def show_data(self, controller, table_name):
        """
        Fetch and display data from the selected table.
        
        :param controller (object): The controller responsible for fetching the table's data.
        :param table_name (str): The name of the table whose data is being fetched.
        """
        self.handle_button_click(table_name)
        
        try:
            data = controller.fetch_all()
        except AttributeError:
            data = []
        
        self.update_content(data, table_name)
        
        self.master.master.content.update_options(table_name)
        
    def handle_button_click(self, table_name):
        """
        Update the visual state of the buttons based on user interaction.
        
        :param table_name (str): The name of the table corresponding to the clicked button.
        """
        if self.active_button:
            self.active_button.configure(fg_color="transparent", text_color="white")

        self.active_button = self.buttons[table_name]
        self.active_button.configure(fg_color="#3B8ED0", text_color="white")
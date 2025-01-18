import customtkinter as ctk

from public.Cars.car_card import CarCard
from public.Employees.employee_card import EmployeeCard
from public.Repairs.repair_card import RepairCard


class Frame(ctk.CTkScrollableFrame):
    """
    Scrollable frame that dynamically displays data using card components.
    """

    def __init__(self, master, **kwargs):
        """
        Initialize the Frame.

        :param master (ctk.CTk): The parent widget for the frame.
        :param kwargs: Additional keyword arguments for the CTkScrollableFrame.
        """
        super().__init__(master, width=650, height=450, **kwargs)

        self.card_classes = {
            "car": CarCard,
            "employee": EmployeeCard,
            "repair": RepairCard
        }


    def update_content(self, data, table_name):
        """
        Update the content of the frame with data from the selected table.

        :param data (list): A list of records to display, where each record is expected to have a `to_dict` method.
        :param table_name (str): The name of the active table, which determines the card type to use.
        """
        for widget in self.winfo_children():
            widget.destroy()
        
        card_class = self.card_classes.get(table_name)
        
        if not card_class:
            label = ctk.CTkLabel(self, text=f"No card class defined for {table_name}.", anchor="center")
            label.pack(expand=True, pady=10)
            return

        for record in data:
            try:
                card = card_class(self, **record.to_dict())
                card.pack(pady=5)               
                
                print(f"Table {table_name} data loaded!")
                
            except TypeError as e:
                print(e)
                label = ctk.CTkLabel(self, text=f"Error creating card: {e}", anchor="center", text_color="red")
                label.pack(expand=True, pady=10)
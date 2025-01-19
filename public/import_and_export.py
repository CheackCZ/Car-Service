import csv

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from tkinter import filedialog

from src.controllers.car_controller import CarController
from src.controllers.employee_controller import EmployeeController
from src.controllers.repair_controller import RepairController


class ImportExport(ctk.CTkFrame):
    """
    Class that provides import and export functionality for table data in the Car Service application.
    """
    
    def __init__(self, parent, get_active_table_callback, repair_controller, employee_controller, car_controller, **kwargs):
        """
        Initialize the ImportExport frame.

        :param parent (ctk.CTk): The parent widget for the ImportExport frame.
        :param get_active_table_callback (callable): A callback function to get the currently active table.
        :param kwargs: Additional keyword arguments for the CTkFrame.
        """
        super().__init__(parent, **kwargs)
        self.get_active_table_callback = get_active_table_callback
        
        self.repair_controller = repair_controller
        self.employee_controller = employee_controller
        self.car_controller = car_controller

        # Import Button
        self.import_button = ctk.CTkButton(self, text="Import", command=self.import_data, border_width=2, border_color="#3B8ED0", fg_color="transparent", corner_radius=20)
        self.import_button.place(x=10, y=10)

        # Export Button
        self.export_button = ctk.CTkButton(self, text="Export", command=self.export_data, border_width=2, border_color="#3B8ED0", fg_color="transparent", corner_radius=20)
        self.export_button.place(x=10, y=50)

        # Placeholder labell when no import and export for specified table
        self.placeholder_label = ctk.CTkLabel(self, text="", wraplength=150)
        self.placeholder_label.place(relx=0.5, rely=0.1)


        self.import_button.place_forget()
        self.export_button.place_forget()


    def import_data(self):  
        """
        Imports data into the currently active table from a CSV file.
        Opens a file dialog to select the CSV file, validates the data, and displays a preview before import.
        """
        active_table = self.get_active_table_callback()
        
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            data = self.read_csv(file_path)
            controller = self.get_controller(active_table)
            controller.validate_import_data(data)

            self.show_preview_popup(data, active_table, controller.import_data)
        except Exception as e:
            print(f"Error importing data: {e}")
            CTkMessagebox(title="Validation Error", message=str(e), icon="warning")
            
    def confirm_import(self, on_confirm, data, popup):
        """
        Confirms the import of data into the active table.
        
        :param on_confirm (callable): The function to call for importing the data.
        :param data (list): The data to import.
        :param popup (ctk.CTkToplevel): The popup window to close after confirmation.
        """
        try:
            on_confirm(data)
            
            print("Data imported successfully.")
        except Exception as e:
            print(f"Error during import of data: {e}")
        finally:
            popup.destroy()
    
    def read_csv(self, file_path):
        """
        Reads a CSV file and returns its data.
        
        :param file_path (str): The path to the CSV file.       

        :return list: A list of dictionaries representing the rows in the CSV file.
        """
        with open(file_path, 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]


    def export_data(self):
        """
        Exports data from the selected table to a CSV file.
        Opens a save dialog for the user to choose the location and filename.
        """
        active_table = self.get_active_table_callback()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Export Data",
        )
        if not file_path:
            return  

        try:
            controller = self.get_controller(active_table)

            data = controller.fetch_all()

            self.write_csv(file_path, data)

            CTkMessagebox(title="Success", message=f"Data exported successfully to {file_path}!", icon="info")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error exporting data: {e}", icon="warning")

    def write_csv(self, file_path, data):
        """
        Writes data to a CSV file.

        :param file_path (str): Path to save the CSV file.
        :param data (list): List of dictionaries representing the data to export.
        """
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            if not data:
                print("No data to export.")
                CTkMessagebox(title="Error", message=f"No data to Export!", icon="warning")
                return

            headers = data[0].to_dict().keys() if hasattr(data[0], 'to_dict') else data[0].keys()

            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            for item in data:
                row = item.to_dict() if hasattr(item, 'to_dict') else item
                writer.writerow(row)


    def get_controller(self, table_name):
        controllers = {
            "car": self.car_controller,
            "employee": self.employee_controller,
            "repair": self.repair_controller,
        }
        
        if table_name not in controllers:
            raise ValueError(f"No controller defined for table {table_name}")
        
        return controllers[table_name]


    def show_preview_popup(self, data, table_name, on_confirm):
        """
        Displays a popup window to preview data before importing.
        
        :param data (list): The data to preview.
        :param table_name (str): The name of the table being imported into.
        :param on_confirm (callable): The function to call for confirming the import.
        """
        popup = ctk.CTkToplevel(self)
        popup.title("Import Preview")
        popup.geometry("400x320")  
        popup.resizable(False, False)

        # "Import data" label
        title_label = ctk.CTkLabel(popup, text=f"Import data to {table_name}", font=("Poppins", 16, "bold"))
        title_label.place(relx = 0.5, rely = 0.05, anchor="n")


        # Table preview
        preview_frame = ctk.CTkFrame(popup, width=380, height=300)
        preview_frame.place(relx=0.5, rely=0.5, anchor="center")

        for i, row in enumerate(data): 
            for j, (key, value) in enumerate(row.items()):
                cell = ctk.CTkLabel(preview_frame, text=value, font=("Arial", 10))
                cell.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")


        # Confirm and Cancel buttons
        cancel_button = ctk.CTkButton(popup, text="Cancel", command=popup.destroy, fg_color="transparent", border_width=2, border_color="#3B8ED0", cursor="hand2")
        cancel_button.place(relx=0.3, rely=0.9, anchor="center")
        
        confirm_button = ctk.CTkButton(popup, text="Confirm Import", font=("Arial", 12, "bold"), command=lambda: self.confirm_import(on_confirm, data, popup))
        confirm_button.place(relx=0.7, rely=0.9, anchor="center")
        
        popup.grab_set()
        popup.lift()

            
    def update_visibility(self, table_name):
        """
        Updates the visibility of the buttons based on the selected table.        
        
        :param table_name (str): The name of the active table.
        """
        supported_tables = {"car", "employee", "repair"}

        if table_name in supported_tables:
            self.import_button.place(x=10, y=10)
            self.export_button.place(x=10, y=50)
            self.placeholder_label.place_forget()
        else:
            self.import_button.place_forget()
            self.export_button.place_forget()
            self.placeholder_label.configure(text=f"Import/Export not supported for {table_name}.")
            self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")
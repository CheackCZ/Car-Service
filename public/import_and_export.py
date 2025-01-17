from tkinter import filedialog
import customtkinter as ctk

import csv
from CTkMessagebox import CTkMessagebox

from src.controllers.car_controller import CarController
from src.controllers.employee_controller import EmployeeController
from src.controllers.repair_controller import RepairController

class ImportExport(ctk.CTkFrame):
    
    def __init__(self, parent, get_active_table_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.get_active_table_callback = get_active_table_callback

        # Import Button
        self.import_button = ctk.CTkButton(self, text="Import", command=self.import_data, border_width=2, border_color="#3B8ED0", fg_color="transparent", corner_radius=20)
        self.import_button.place(x=10, y=10)

        # Export Button
        self.export_button = ctk.CTkButton(self, text="Export", command=self.export_data, border_width=2, border_color="#3B8ED0", fg_color="transparent", corner_radius=20)
        self.export_button.place(x=10, y=50)

        self.placeholder_label = ctk.CTkLabel(self, text="", wraplength=150)
        self.placeholder_label.place(relx=0.5, rely=0.1)



    def import_data(self):
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

    def confirm_import(self, on_confirm, data, popup):
        try:
            on_confirm(data)
            print("Data imported successfully.")
        except Exception as e:
            print(f"Error during import: {e}")
        finally:
            popup.destroy()
            
    def read_csv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]


    def export_data(self):
        """
        Exports data from the selected table to a CSV file.
        Opens a save dialog for the user to choose the location and filename.
        """
        active_table = self.get_active_table_callback()

        # Open save dialog to choose the file location and name
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Export Data",
        )
        if not file_path:
            return  # User canceled the save dialog

        try:
            # Get the relevant controller for the active table
            controller = self.get_controller(active_table)

            # Fetch all data from the active table
            data = controller.fetch_all()

            # Write data to the CSV file
            self.write_csv(file_path, data)

            CTkMessagebox(title="Success", message=f"Data exported successfully to {file_path}!", icon="info")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Error exporting data: {e}", icon="warning")

    def write_csv(self, file_path, data):
        """
        Writes data to a CSV file.

        :param file_path: Path to save the CSV file.
        :param data: List of dictionaries representing the data to export.
        """
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            if not data:
                print("No data to export.")
                return

            # Get the headers from the first row's keys
            headers = data[0].to_dict().keys() if hasattr(data[0], 'to_dict') else data[0].keys()

            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            for item in data:
                row = item.to_dict() if hasattr(item, 'to_dict') else item
                writer.writerow(row)




    def get_controller(self, table_name):
        controllers = {
            "car": CarController,
            "employee": EmployeeController,
            "repair": RepairController,
        }
        if table_name not in controllers:
            raise ValueError(f"No controller defined for table {table_name}")
        return controllers[table_name]


    def show_preview_popup(self, data, table_name, on_confirm):
        popup = ctk.CTkToplevel(self)
        popup.title("Import Preview")
        popup.geometry("400x320")  # Reduced width and height
        popup.resizable(False, False)

        # Add "Import data" label
        title_label = ctk.CTkLabel(popup, text=f"Import data to {table_name}", font=("Poppins", 16, "bold"))
        title_label.place(relx = 0.5, rely = 0.05, anchor="n")

        # Add table preview
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

            
    def update_visibility(self, table_name):
        """
        Updates the visibility of the buttons based on the selected table.
        """
        supported_tables = {"car", "employee", "repair"}  # Tables with controllers

        if table_name in supported_tables:
            self.import_button.place(x=10, y=10)
            self.export_button.place(x=10, y=50)
            self.placeholder_label.place_forget()
        else:
            # Hide buttons and show placeholder text
            self.import_button.place_forget()
            self.export_button.place_forget()
            self.placeholder_label.configure(
                text=f"Import/Export not supported for {table_name}."
            )
            self.placeholder_label.place(relx=0.5, rely=0.5, anchor="center")
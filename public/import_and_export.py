import customtkinter as ctk
from tkinter import filedialog

class ImportExport(ctk.CTkFrame):
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Import Button
        self.import_button = ctk.CTkButton(self, text="Import", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", command=self.open_file_dialog, cursor="hand2")
        self.import_button.place(x=10, y=10)

        # Export Button
        self.export_button = ctk.CTkButton(self, text="Export", border_width=2, border_color="#3B8ED0", corner_radius=20, fg_color="transparent", cursor="hand2")
        self.export_button.place(x=10, y=50)
        
        
    def open_file_dialog(self):
        # Open a file dialog to select a file
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("CSV Files", "*.csv")]
        )
        
        if file_path:
            print(f"Selected file: {file_path}")
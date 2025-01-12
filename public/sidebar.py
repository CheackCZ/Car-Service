import customtkinter as ctk
from tkinter import ttk

class Sidebar(ctk.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, width=180, height=480, **kwargs)

        # Label with database name
        self.db_name_label = ctk.CTkLabel(self, text="Service", font=("Poppins", 16, "bold"), text_color="white", wraplength=160, justify="left")
        self.db_name_label.place(x = 10, y = 20)
        
        # Scrollable frame with all tables in given database
        self.tables_container = ctk.CTkScrollableFrame(self, width=140, height=self.tables_container_height())
        self.tables_container.place(x = 10, y = self.tables_container_y())
        
        # Treeview with the tables and its attibutes in the scrollable frame
        self.treeview = ttk.Treeview(self.tables_container, height=6, show="tree")
        self.treeview.grid()
        self.style_treeview()
        
        # Insert data
        self.treeview.insert('', '0', 'i1', text ='Python')
        self.treeview.insert('', '1', 'i2', text ='Customtkinter')
        self.treeview.insert('', '2', 'i3', text ='Tkinter')
        self.treeview.insert('i2', 'end', 'Frame', text ='Frame')
        self.treeview.insert('i2', 'end', 'Label', text ='Label')
        self.treeview.insert('i3', 'end', 'Treeview', text ='Treeview')
        self.treeview.move('i2', 'i1', 'end')
        self.treeview.move('i3', 'i1', 'end')
        
    def tables_container_height(self):
        self.update_idletasks()
        db_name_height = self.db_name_label.winfo_height()
        calculated_height = self._current_height - (db_name_height + 50)
        return calculated_height
    
    def tables_container_y(self):
        db_name_y = self.db_name_label.winfo_y() 
        db_name_height = self.db_name_label.winfo_height()  
        
        return db_name_y + db_name_height + 10
    
    
    def style_treeview(self):
        bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkScrollableFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure(
            "Treeview", 
            background=bg_color, 
            foreground=text_color, 
            fieldbackground=bg_color, 
            borderwidth=0
        )
        treestyle.map(
            "Treeview", 
            background=[("selected", selected_color)], 
            foreground=[("selected", text_color)]
        )
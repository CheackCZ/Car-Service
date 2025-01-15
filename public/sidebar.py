import customtkinter as ctk

from tables import Tables

class Sidebar(ctk.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, width=180, height=560, **kwargs)
        
        # Label with database name
        self.db_name_label = ctk.CTkLabel(self, text="Service", font=("Poppins", 16, "bold"), text_color="white", wraplength=160, justify="left")
        self.db_name_label.place(x=10, y=20)
        
        # Scrollable frame with all tables in given database
        self.tables_container = Tables(master=self)
        self.tables_container.place(x = 10, y = 50)

        # Exit Button
        self.exit_button = ctk.CTkButton(self, text="Exit", fg_color="red", text_color="white", hover_color="#FF474D", cursor="hand2", command=self.exit_application)
        self.exit_button.place(relx=0.5, rely=1.0, anchor="s", y=-30)
        
    def exit_application(self):
        self.master.destroy()
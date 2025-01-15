import customtkinter as ctk

from public.Employees.employee_card import EmployeeCard

class EmployeesFrame(ctk.CTkScrollableFrame):
    
     def __init__(self, master, **kwargs):
        super().__init__(master, width=650, height=450, **kwargs)
        
        # Content showing the values in the given table
        self.employee1 = EmployeeCard(self, "Ondřej", "Martin", "Faltin", "+420 774 102 991", "ondra.faltin@gmail.com", cursor="hand2")
        self.employee1.pack(pady=5, padx=5, anchor="w")  
        
        # Content showing the values in the given table
        self.employee2 = EmployeeCard(self, "Tomáš", "Negr", "Kléger", "+420 111 222 333", "thastertzyn@thastertyn.xyz", cursor="hand2")
        self.employee2.pack(pady=5, padx=5, anchor="w")  
        
        # Content showing the values in the given table
        self.employee3 = EmployeeCard(self, "Denis", "Jan", "heim", "+420 999 888 777", "denish.hem@kratom.cz", cursor="hand2")
        self.employee3.pack(pady=5, padx=5, anchor="w")  
        
        # Content showing the values in the given table
        self.employee3 = EmployeeCard(self, "Denis", "Jan", "heim", "+420 999 888 777", "denish.hem@kratom.cz", cursor="hand2")
        self.employee3.pack(pady=5, padx=5, anchor="w")  
        
        # Content showing the values in the given table
        self.employee3 = EmployeeCard(self, "Denis", "Jan", "heim", "+420 999 888 777", "denish.hem@kratom.cz", cursor="hand2")
        self.employee3.pack(pady=5, padx=5, anchor="w")  
        
        # Content showing the values in the given table
        self.employee3 = EmployeeCard(self, "Denis", "Jan", "heim", "+420 999 888 777", "denish.hem@kratom.cz", cursor="hand2")
        self.employee3.pack(pady=5, padx=5, anchor="w")  
        
        # Content showing the values in the given table
        self.employee3 = EmployeeCard(self, "Denis", "Jan", "heim", "+420 999 888 777", "denish.hem@kratom.cz", cursor="hand2")
        self.employee3.pack(pady=5, padx=5, anchor="w")  
        
        # Content showing the values in the given table
        self.employee3 = EmployeeCard(self, "Denis", "Jan", "heim", "+420 999 888 777", "denish.hem@kratom.cz", cursor="hand2")
        self.employee3.pack(pady=5, padx=5, anchor="w")  
        
        # Content showing the values in the given table
        self.employee3 = EmployeeCard(self, "Denis", "Jan", "heim", "+420 999 888 777", "denish.hem@kratom.cz", cursor="hand2")
        self.employee3.pack(pady=5, padx=5, anchor="w")  
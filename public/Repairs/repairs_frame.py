import customtkinter as ctk

from public.Repairs.repair_card import RepairCard

class RepairsFrame(ctk.CTkScrollableFrame):
    
     def __init__(self, master, **kwargs):
        super().__init__(master, width=650, height=450, **kwargs)
        
        # Content showing the values in the given table
        self.repair1 = RepairCard(self, 1, "Ondřej Faltin", 1, "Octavia", "5AS 9653", "ŠKODA", "Oprava podvozku", "23.06.2024", "29.11.2024", 21000, "HOTOVO", cursor="hand2")
        self.repair1.pack(pady=5, padx=5, anchor="w")  
         
        # Content showing the values in the given table
        self.repair2 = RepairCard(self, 1, "Ondřej Faltin", 1, "Octavia", "5AS 9653", "ŠKODA", "Oprava podvozku", "23.06.2024", "29.11.2024", 21000, "HOTOVO", cursor="hand2")
        self.repair2.pack(pady=5, padx=5, anchor="w")  
        
        # Content showing the values in the given table
        self.repair3 = RepairCard(self, 1, "Ondřej Faltin", 1, "Octavia", "5AS 9653", "ŠKODA", "Oprava podvozku", "23.06.2024", "29.11.2024", 21000, "Probíhá", cursor="hand2")
        self.repair3.pack(pady=5, padx=5, anchor="w")  
import customtkinter as ctk


class SearchBar(ctk.CTkFrame):
    def __init__(self, parent, on_search=None, placeholder_text="Type your query here..."):
        super().__init__(parent, fg_color="transparent", width=840, height=30)
        
        # Entry field for the search query
        self.search_entry = ctk.CTkEntry(self, placeholder_text=placeholder_text, font=("Poppins", 14), width=670)
        self.search_entry.place(x=10, y=0)

        # Search button
        self.search_button = ctk.CTkButton(self, text="Search", font=("Poppins", 14), command=on_search, cursor="hand2")
        self.search_button.place(x = 700, y=0)

        # Assign the external search handler if provided
        self.on_search = on_search
import customtkinter as ctk


class SearchBar(ctk.CTkFrame):
    """
    Class representing a search bar component for the Car Service application.
    
    Note: This class is not implemented and does not funtion properly. 
    """
    
    def __init__(self, parent, on_search=None, placeholder_text="Type here..."):
        """
        Initialize the SearchBar.
        
        :param parent (ctk.CTk): The parent widget for the SearchBar.
        :param on_search (callable, optional): A callback function to execute when the search button is pressed.
        :param placeholder_text (str): The placeholder text for the search entry field.
        """
        super().__init__(parent, fg_color="transparent", width=840, height=30)
        
        self.on_search = on_search
        
        # Entry field for the search query
        self.search_entry = ctk.CTkEntry(self, placeholder_text=placeholder_text, font=("Poppins", 14), width=670)
        self.search_entry.place(x=10, y=0)

        # Search button
        self.search_button = ctk.CTkButton(self, command=self._search, text="Search", font=("Poppins", 14), cursor="hand2")
        self.search_button.place(x=700, y=0)
        

    def _search(self):
        if self.on_search:
            query = self.search_entry.get().strip()
            self.on_search(query)
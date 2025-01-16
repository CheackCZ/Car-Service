

class Brand():
    """
    Class representing individual (Car) brands in the database.
    """
    
    def __init__(self, id: int = 0, name: str = ""):
        """
        Initializes Car instance.
        
        :param name (str): car brand's name.
        """        
        # Validate id
        if type(id) != int or id < 0:
            raise ValueError("'id' must be a positive integer.")
        
        # Validate name (allow default empty string)
        if type(name) != str or len(name) > 50:
            raise ValueError("Name must be a string with a maximum of 50 characters.")

        self.id = id
        self.name = name
        
    def __str__(self):
        return f"({self.id}) {self.name}"
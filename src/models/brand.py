

class Brand():
    """
    Class representing individual (Car) brands in the database.
    """
    
    def __init__(self, id: int, name: str):
        """
        Initializes Car instance.
        
        :param name (str): car brand's name.
        """        
        # Validate id
        if type(id) != int or id <= 0:
            raise ValueError("'id' must be a positive integer.")
        
        # Validate name
        if not name or type(name) != str or len(name) > 50:
            raise ValueError("Name must be a non-empty string with a maximum of 50 characters.")

        self.id = id
        self.name = name
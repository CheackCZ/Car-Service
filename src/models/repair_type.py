

class RepairType():
    """
    Class representing individual Repair types in the database.
    """
    
    def __init__(self, id: int = 0, name: str = "", description: str = ""):
        """
        Initializes RepairType instance.
        
        :param name (str): The name of the repair type. Must be a non-empty string with a maximum length of 50 characters.
        :param description (str): A description of the repair type. Must be a string with a maximum length of 255 characters.
        """        
        # Validate id
        if type(id) != int or id < 0:
            raise ValueError("'id' must be a positive integer.")
        
        # Validate name
        if type(name) != str or len(name) > 50:
            raise ValueError("Name must be a string with a maximum of 50 characters.")

        # Validate description
        if type(description) != str or len(description) > 255:
            raise ValueError("Description must be a string with a maximum of 500 characters.")

        self.id = id
        self.name = name
        self.description = description
        
    
    def __str__(self):
        return f"({self.id}) {self.name}: {self.description}"
    
    def to_dict(self):
        """
        Converts the RepairType object into a dictionary representation.
        
        :return: Dictionary representation of the RepairType object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
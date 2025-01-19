
class DirtyReading():

    def __init__(self, table_name, session_id):
        if type(table_name) != str:
            raise ValueError("'table_name' must be a string.")

        self.table_name = table_name
        self.session_id = session_id
    
    def __str__(self):
        return f"Dirty reading for {self.table_name} is {'ON' if self.is_dirty_reading_on else 'OFF'}"
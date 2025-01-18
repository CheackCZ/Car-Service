import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from src.controllers.car_controller import CarController

class CarSelector(ctk.CTkToplevel):
    """
    A class for displaying a dropdown (combobox) of cars with their IDs.
    """
    
    def __init__(self, parent, on_submit_callback, title="Choose Car", button_text="Submit", **kwargs):
        """
        Initialize the CarSelector window.

        :param parent: Parent widget.
        :param on_submit_callback: Callback function to handle selection submission.
        :param title: Window title.
        :param button_text: Text for the submit button.
        :param kwargs: Additional arguments for the CTkFrame.
        """
        super().__init__(parent, **kwargs)

        self.car_data = {}
        self.selected_car_id = None
        self.on_submit_callback = on_submit_callback

        # Window properties
        self.title(title)
        self.geometry("260x180")
        self.resizable(False, False)

        # Label for car selection
        self.label = ctk.CTkLabel(self, text="Car Selection", text_color="white", font=("Poppins", 16, "bold"))
        self.label.place(relx=0.5, y=30, anchor="center")

        # ComboBox for car selection
        self.combobox = ctk.CTkComboBox(self, width=200, values=[])
        self.combobox.place(relx=0.5, y=70, anchor="center")

        # Submit button
        self.submit_button = ctk.CTkButton(self, text=button_text, command=self.submit_selection)
        self.submit_button.place(relx=0.5, y=130, anchor="center")

        self.load_cars()
        

    def load_cars(self):
        """
        Load cars from the database and populate the combobox.
        """
        try:
            cars = CarController.fetch_all()

            self.car_data = {
                f"({car.id}) {car.brand.name} {car.model} - {car.registration_number}": car.id
                for car in cars
            }

            self.combobox.configure(values=list(self.car_data.keys()))

            self.combobox.set("")
        except Exception as e:
            print(f"Error loading cars: {e}")

    def submit_selection(self):
        """
        Handle the submission of the selected car.
        """
        selected_text = self.combobox.get()
        self.selected_car_id = self.car_data.get(selected_text)
        
        if self.selected_car_id:
            self.on_submit_callback(self.selected_car_id)
            self.destroy()
        else:
            CTkMessagebox(title="Error", message="No car selected.", icon="warning")
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class RepairSelector(ctk.CTkToplevel):
    """
    A class for displaying a dropdown (combobox) of repairs with their IDs.
    """
    
    def __init__(self, parent, on_submit_callback, controller, title="Choose Repair", button_text="Submit", **kwargs):
        """
        Initialize the RepairSelector window.

        :param parent: Parent widget.
        :param on_submit_callback: Callback function to handle selection submission.
        :param title: Window title.
        :param button_text: Text for the submit button.
        :param kwargs: Additional arguments for the CTkFrame.
        """
        super().__init__(parent, **kwargs)

        self.repair_data = {}
        self.selected_repair_id = None
        self.on_submit_callback = on_submit_callback

        self.repair_controller = controller

        # Window properties
        self.title(title)
        self.geometry("260x180")
        self.resizable(False, False)

        # Label for repair selection
        self.label = ctk.CTkLabel(self, text="Repair Selection", text_color="white", font=("Poppins", 16, "bold"))
        self.label.place(relx=0.5, y=30, anchor="center")

        # ComboBox for repair selection
        self.combobox = ctk.CTkComboBox(self, width=200, values=[])
        self.combobox.place(relx=0.5, y=70, anchor="center")

        # Submit button
        self.submit_button = ctk.CTkButton(self, text=button_text, command=self.submit_selection)
        self.submit_button.place(relx=0.5, y=130, anchor="center")

        self.load_repairs()

    def load_repairs(self):
        """
        Load repairs from the database and populate the combobox.
        """
        try:
            repairs = self.repair_controller.fetch_all()

            self.repair_data = {
                f"({repair.id}) {repair.repair_type.name}": repair.id
                for repair in repairs
            }

            self.combobox.configure(values=list(self.repair_data.keys()))

            self.combobox.set("")
        except Exception as e:
            print(f"Error loading repairs: {e}")

    def submit_selection(self):
        """
        Handle the submission of the selected repair.
        """
        selected_text = self.combobox.get()
        self.selected_repair_id = self.repair_data.get(selected_text)
        
        if self.selected_repair_id:
            self.on_submit_callback(self.selected_repair_id)
            self.destroy()
        else:
            CTkMessagebox(title="Error", message="No repair selected.", icon="warning")

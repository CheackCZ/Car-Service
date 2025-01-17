import customtkinter as ctk
from tkinter import filedialog

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from src.report_generator import ReportGenerator

from .tables import Tables

class Sidebar(ctk.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, width=180, height=560, **kwargs)
        
        # Label with database name
        self.db_name_label = ctk.CTkLabel(self, text="Service", font=("Poppins", 16, "bold"), text_color="white", wraplength=160, justify="left")
        self.db_name_label.place(x=10, y=20)
        
        # Scrollable frame with all tables in given database
        self.tables_container = Tables(master=self)
        self.tables_container.place(x = 10, y = 50)
        
        # Report button
        self.report_button = ctk.CTkButton(self, text="Create report", command=self.create_report, cursor="hand2")
        self.report_button.place(relx=0.5, rely=1.0, anchor="s", y=-70)

        # Exit Button
        self.exit_button = ctk.CTkButton(self, text="Exit", fg_color="red", text_color="white", hover_color="#FF474D", cursor="hand2", command=self.exit_application)
        self.exit_button.place(relx=0.5, rely=1.0, anchor="s", y=-30)
        
        
    def create_report(self):
        """
        Fetches and displays the summary report.
        """
        try:
            report_data = ReportGenerator.generate_summary_report()
            self.display_report_popup(report_data)
        except Exception as e:
            print(f"Error generating report: {e}")

    def display_report_popup(self, data):
        """
        Displays the report in a popup window and generates a PDF file.
        :param data: List of dictionaries with report data.
        """
        popup = ctk.CTkToplevel(self)
        popup.title("Summary Report")
        popup.geometry("600x400")
        popup.resizable(False, False)

        # Title label
        title_label = ctk.CTkLabel(popup, text="Summary Report", font=("Poppins", 18, "bold"))
        title_label.pack(pady=10)

        # Report data display
        text_widget = ctk.CTkTextbox(popup, wrap="word", width=540, height=280)
        text_widget.pack(pady=10)

        # Populate report data
        for row in data:
            text_widget.insert("end", f"Employee: {row['employee_name']}\n")
            text_widget.insert("end", f"  Total Repairs: {row['total_repairs']}\n")
            text_widget.insert("end", f"  Average Price: {row['average_repair_price']:.2f}\n")
            text_widget.insert("end", f"  Max Price: {row['max_repair_price']:.2f}\n")
            text_widget.insert("end", f"  Min Price: {row['min_repair_price']:.2f}\n")
            text_widget.insert("end", f"  Repairs Per Employee: {row['repairs_per_employee']}\n")
            text_widget.insert("end", f"  Cars Delivered: {row['cars_delivered']}\n\n")
        text_widget.configure(state="disabled")

        # Frame for buttons
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=10)

        # Generate PDF button
        generate_pdf_button = ctk.CTkButton(button_frame, text="Generate PDF", command=lambda: self.generate_pdf(data))
        generate_pdf_button.pack(side="right", padx=10)

        # Close button
        close_button = ctk.CTkButton(button_frame, text="Close", fg_color="transparent", border_width=2, border_color="#3B8ED0", command=popup.destroy)
        close_button.pack(side="left", padx=10)
        
        popup.grab_set()
        popup.lift()


    def generate_pdf(self, data):
        """
        Generates a PDF file with the report data.
        :param data: List of dictionaries with report data.
        """
        # Open file dialog to choose save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Report as PDF",
        )
        if not file_path:
            return  # User canceled the save dialog

        try:
            # Create PDF canvas
            pdf = canvas.Canvas(file_path, pagesize=letter)
            pdf.setFont("Helvetica", 12)
            y = 750

            # Title
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(50, y, "Summary Report")
            y -= 30

            # Add report data
            pdf.setFont("Helvetica", 12)
            for row in data:
                pdf.drawString(50, y, f"Employee: {row['employee_name']}")
                y -= 20
                pdf.drawString(70, y, f"Total Repairs: {row['total_repairs']}")
                y -= 20
                pdf.drawString(70, y, f"Average Price: {row['average_repair_price']:.2f}")
                y -= 20
                pdf.drawString(70, y, f"Max Price: {row['max_repair_price']:.2f}")
                y -= 20
                pdf.drawString(70, y, f"Min Price: {row['min_repair_price']:.2f}")
                y -= 20
                pdf.drawString(70, y, f"Repairs Per Employee: {row['repairs_per_employee']}")
                y -= 20
                pdf.drawString(70, y, f"Cars Delivered: {row['cars_delivered']}")
                y -= 40

                # Start a new page if content overflows
                if y < 50:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 12)
                    y = 750

            pdf.save()
            print(f"Report saved as PDF at {file_path}.")
        except Exception as e:
            print(f"Error generating PDF: {e}")

    def exit_application(self):
        self.master.destroy()
import customtkinter as ctk

class MainWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.create_widgets()

    def create_widgets(self):
        # Example layout: header + 3 buttons + area to display forecast
        header = ctk.CTkLabel(self, text="Financial Planner", font=("Helvetica", 18))
        header.pack(pady=20)

        # Buttons
        add_income_btn = ctk.CTkButton(self, text="Add Income", command=self.add_income)
        add_expense_btn = ctk.CTkButton(self, text="Add Expense", command=self.add_expense)
        forecast_btn = ctk.CTkButton(self, text="Forecast Balance", command=self.forecast)

        add_income_btn.pack(pady=5)
        add_expense_btn.pack(pady=5)
        forecast_btn.pack(pady=20)

        # Output area (you can replace with text box, frame, etc.)
        self.output_label = ctk.CTkLabel(self, text="Forecast will appear here")
        self.output_label.pack(pady=10)

    def add_income(self):
        print("Add income clicked")  # Hook up to a popup or form later

    def add_expense(self):
        print("Add expense clicked")

    def forecast(self):
        print("Forecast clicked")

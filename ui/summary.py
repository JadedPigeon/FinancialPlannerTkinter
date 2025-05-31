import customtkinter as ctk

class SummaryWindow(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        title_label = ctk.CTkLabel(self, text="Financial Summary Dashboard")
        title_label.pack()

        current_balance_label = ctk.CTkLabel(self, text="Current Balance: $0.00")
        current_balance_label.pack(side="left", padx=10, pady=10)
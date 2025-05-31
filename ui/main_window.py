import customtkinter as ctk
from tkinter import simpledialog

class MainWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)

        title_label = ctk.CTkLabel(self, text="Python Financial Planner", font=("Arial", 24))
        title_label.pack()

        self.current_balance = 0.00  # This would be dynamically updated in a real application
        self.current_balance_label = ctk.CTkLabel(self, text=f"Current Balance: ${self.current_balance:.2f}", font=("Arial", 16))
        self.current_balance_label.pack()
        update_balance_button = ctk.CTkButton(self, text="Update Balance", command=self.update_balance)
        update_balance_button.pack()

    def update_balance(self):
        print("update_balance called")

        update_balance_window = ctk.CTkToplevel(self.winfo_toplevel())
        update_balance_window.title("Update Current Balance")
        update_balance_window.geometry("300x125")

        label = ctk.CTkLabel(update_balance_window, text="Enter current balance:")
        label.pack(pady=1)  # Top and bottom padding

        error_label = ctk.CTkLabel(update_balance_window, text="", text_color="red")
        error_label.pack(pady=1)

        entry = ctk.CTkEntry(update_balance_window)
        entry.pack(pady=1)
        entry.focus()
        entry.bind("<Return>", lambda event: submit())
        entry.bind("<KP_Enter>", lambda event: submit())

        def submit():
            value = entry.get()
            try:
                self.current_balance = float(value)
                self.current_balance_label.configure(
                    text=f"Current Balance: ${self.current_balance:.2f}"
                )
                update_balance_window.destroy()
            except ValueError:
                error_label.configure(text="Please enter a valid number.")

        button = ctk.CTkButton(update_balance_window, text="Submit", command=submit)
        button.pack(pady=1)  # Top and bottom padding

        update_balance_window.update()
        update_balance_window.grab_set()
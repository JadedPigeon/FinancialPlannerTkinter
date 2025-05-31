import customtkinter as ctk
from datetime import datetime
from tkcalendar import Calendar

class MainWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(self, text="Python Financial Planner", font=("Arial", 24))
        title_label.pack(pady=1)

        # Current Balance
        self.current_balance = 0.00  # This would be dynamically updated in a real application
        self.current_balance_label = ctk.CTkLabel(self, text=f"Current Balance: ${self.current_balance:.2f}")
        self.current_balance_label.pack(pady=1)
        self.update_balance_button = ctk.CTkButton(self, text="Update Balance", command=self.update_balance)
        self.update_balance_button.pack(pady=1)

        # Current Date
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.current_date_label = ctk.CTkLabel(self, text=f"Current Date: {self.current_date}")
        self.current_date_label.pack(pady=1)

        # Target Date
        self.pick_date_btn = ctk.CTkButton(self, text="Pick Target Date", command=self.open_date_picker)
        self.pick_date_btn.pack(pady=1)

        self.target_label = ctk.CTkLabel(self, text="Target Date: Not set")
        self.target_label.pack(pady=1)

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

    def open_date_picker(self):
        target_date_window = ctk.CTkToplevel()
        target_date_window.geometry("300x250")
        target_date_window.title("Select Target Date")

        def set_date():
            selected_date = cal.get_date()
            self.target_label.configure(text=f"Target Date: {selected_date}")
            target_date_window.destroy()

        cal = Calendar(target_date_window, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=1)

        confirm_btn = ctk.CTkButton(target_date_window, text="Set Date", command=set_date)
        confirm_btn.pack(pady=1)

        target_date_window.update()
        target_date_window.grab_set()


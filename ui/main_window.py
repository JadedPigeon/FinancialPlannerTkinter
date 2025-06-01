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

        # Recurring income
        self.recurring_income_label = ctk.CTkLabel(self, text="Recurring Income:")
        self.recurring_income_label.pack(pady=1)

        self.add_income_button = ctk.CTkButton(self, text="Add Recurring Income", command=self.add_recurring_income)
        self.add_income_button.pack(pady=1)

        self.recurring_income_list = []
        self.recurring_income_display = ctk.CTkLabel(self, text="")
        self.recurring_income_display.pack(pady=1)

        # Recurring expenses
        self.recurring_expenses_label = ctk.CTkLabel(self, text="Recurring Expenses:")
        self.recurring_expenses_label.pack(pady=1)

        self.add_expense_button = ctk.CTkButton(self, text="Add Recurring Expense", command=self.add_recurring_expense)
        self.add_expense_button.pack(pady=1)

        self.recurring_expenses_list = []
        self.recurring_expenses_display = ctk.CTkLabel(self, text="")
        self.recurring_expenses_display.pack(pady=1)


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
            if cal.get_date() <  self.current_date:
                print("Selected date is in the past. Please select a future date.")
                return
            selected_date = cal.get_date()
            self.target_label.configure(text=f"Target Date: {selected_date}")
            target_date_window.destroy()

        cal = Calendar(target_date_window, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=1)

        confirm_btn = ctk.CTkButton(target_date_window, text="Set Date", command=set_date)
        confirm_btn.pack(pady=1)

        target_date_window.update()
        target_date_window.grab_set()

    def add_recurring_income(self):
        popup = ctk.CTkToplevel(self.winfo_toplevel())
        popup.title("Add Recurring Income")
        popup.geometry("300x250")

        label_amount = ctk.CTkLabel(popup, text="Amount:")
        label_amount.pack(pady=1)
        entry_amount = ctk.CTkEntry(popup)
        entry_amount.pack(pady=1)

        label_freq = ctk.CTkLabel(popup, text="Frequency:")
        label_freq.pack(pady=1)
        freq_var = ctk.StringVar(value="Monthly")
        freq_menu = ctk.CTkOptionMenu(popup, variable=freq_var, values=["Weekly", "Biweekly", "Monthly"])
        freq_menu.pack(pady=1)

        start_date_var = ctk.StringVar(value="Not set")
        def pick_start_date():
            cal_win = ctk.CTkToplevel(popup)
            cal_win.title("Pick Start Date")
            cal_win.geometry("300x250")
            cal = Calendar(cal_win, selectmode='day', date_pattern='yyyy-mm-dd')
            cal.pack(pady=1)
            def set_date():
                start_date_var.set(cal.get_date())
                start_date_label.configure(text=f"Start Date: {start_date_var.get()}")
                cal_win.destroy()
            ctk.CTkButton(cal_win, text="Set Date", command=set_date).pack(pady=1)
            cal_win.update()
            cal_win.grab_set()

        pick_date_btn = ctk.CTkButton(popup, text="Pick Start Date", command=pick_start_date)
        pick_date_btn.pack(pady=1)
        start_date_label = ctk.CTkLabel(popup, text="Start Date: Not set")
        start_date_label.pack(pady=1)

        def submit():
                try:
                    amount = float(entry_amount.get())
                    freq = freq_var.get()
                    start_date = start_date_var.get()
                    if start_date == "Not set":
                        error_label.configure(text="Please pick a start date.")
                        return
                    self.recurring_income_list.append((amount, freq, start_date))
                    self.update_recurring_income_display()
                    popup.destroy()
                except ValueError:
                    error_label.configure(text="Please enter a valid amount.")


        submit_btn = ctk.CTkButton(popup, text="Add", command=submit)
        submit_btn.pack(pady=1)

        error_label = ctk.CTkLabel(popup, text="", text_color="red")
        error_label.pack(pady=1)

        popup.update()
        popup.grab_set()

    def update_recurring_income_display(self):
        if not self.recurring_income_list:
            self.recurring_income_display.configure(text="")
        else:
            text = "\n".join([f"${amt:.2f} - {freq} - {date}" for amt, freq, date in self.recurring_income_list])
            self.recurring_income_display.configure(text=text)

    def add_recurring_expense(self):
        popup = ctk.CTkToplevel(self.winfo_toplevel())
        popup.title("Add Recurring Expense")
        popup.geometry("300x250")

        label_amount = ctk.CTkLabel(popup, text="Amount:")
        label_amount.pack(pady=1)
        entry_amount = ctk.CTkEntry(popup)
        entry_amount.pack(pady=1)

        label_freq = ctk.CTkLabel(popup, text="Frequency:")
        label_freq.pack(pady=1)
        freq_var = ctk.StringVar(value="Monthly")
        freq_menu = ctk.CTkOptionMenu(popup, variable=freq_var, values=["Weekly", "Biweekly", "Monthly"])
        freq_menu.pack(pady=1)

        start_date_var = ctk.StringVar(value="Not set")
        def pick_start_date():
            cal_win = ctk.CTkToplevel(popup)
            cal_win.title("Pick Start Date")
            cal_win.geometry("300x250")
            cal = Calendar(cal_win, selectmode='day', date_pattern='yyyy-mm-dd')
            cal.pack(pady=1)
            def set_date():
                start_date_var.set(cal.get_date())
                start_date_label.configure(text=f"Start Date: {start_date_var.get()}")
                cal_win.destroy()
            ctk.CTkButton(cal_win, text="Set Date", command=set_date).pack(pady=1)
            cal_win.update()
            cal_win.grab_set()

        pick_date_btn = ctk.CTkButton(popup, text="Pick Start Date", command=pick_start_date)
        pick_date_btn.pack(pady=1)
        start_date_label = ctk.CTkLabel(popup, text="Start Date: Not set")
        start_date_label.pack(pady=1)

        def submit():
                try:
                    amount = float(entry_amount.get())
                    freq = freq_var.get()
                    start_date = start_date_var.get()
                    if start_date == "Not set":
                        error_label.configure(text="Please pick a start date.")
                        return
                    self.recurring_expenses_list.append((amount, freq, start_date))
                    self.update_recurring_expenses_display()
                    popup.destroy()
                except ValueError:
                    error_label.configure(text="Please enter a valid amount.")


        submit_btn = ctk.CTkButton(popup, text="Add", command=submit)
        submit_btn.pack(pady=1)

        error_label = ctk.CTkLabel(popup, text="", text_color="red")
        error_label.pack(pady=5)

        def submit():
            try:
                amount = float(entry_amount.get())
                freq = freq_var.get()
                self.recurring_expenses_list.append((amount, freq))
                self.update_recurring_expenses_display()
                popup.destroy()
            except ValueError:
                error_label.configure(text="Please enter a valid amount.")

        popup.update()
        popup.grab_set()

    def update_recurring_expenses_display(self):
        if not self.recurring_expenses_list:
            self.recurring_expenses_display.configure(text="")
        else:
            text = "\n".join([f"${amt:.2f} - {freq} - {date}" for amt, freq, date in self.recurring_expenses_list])
            self.recurring_expenses_display.configure(text=text)
import customtkinter as ctk
from datetime import datetime
from tkcalendar import Calendar
import json

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

        self.add_income_button = ctk.CTkButton(self, text="Add Recurring Income", command=lambda: self.add_or_edit_recurring_item(
            self.recurring_income_list, self.recurring_income_display_frame, "Add Recurring Income"))
        self.add_income_button.pack(pady=1)

        self.recurring_income_list = []
        self.recurring_income_display_frame = ctk.CTkFrame(self)
        self.recurring_income_display_frame.pack(pady=1)
        self.update_recurring_items_display(
            self.recurring_income_list,
            self.recurring_income_display_frame,
            lambda idx: self.on_recurring_item_click(
                self.recurring_income_list,
                self.recurring_income_display_frame,
                "Edit Recurring Income",
                idx
            )
        )

        # Recurring expenses
        self.recurring_expenses_label = ctk.CTkLabel(self, text="Recurring Expenses:")
        self.recurring_expenses_label.pack(pady=1)

        self.add_expense_button = ctk.CTkButton(self, text="Add Recurring Expense", command=lambda: self.add_or_edit_recurring_item(
            self.recurring_expenses_list, self.recurring_expenses_display_frame, "Add Recurring Expense"))
        self.add_expense_button.pack(pady=1)

        self.recurring_expenses_list = []
        self.recurring_expenses_display_frame = ctk.CTkFrame(self)
        self.recurring_expenses_display_frame.pack(pady=1)
        self.update_recurring_items_display(
            self.recurring_expenses_list,
            self.recurring_expenses_display_frame,
            lambda idx: self.on_recurring_item_click(
                self.recurring_expenses_list,
                self.recurring_expenses_display_frame,
                "Edit Recurring Expense",
                idx
            )
        )

        # Save
        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_data)
        self.save_button.pack(pady=1)

    def update_balance(self):

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

    def add_or_edit_recurring_item(self, item_list, display_label, title, existing=None, index=None):
        popup = ctk.CTkToplevel(self.winfo_toplevel())
        popup.title(title)
        popup.geometry("300x350")

        label_name = ctk.CTkLabel(popup, text="Recurring Item Name:")
        label_name.pack(pady=1)
        entry_name = ctk.CTkEntry(popup)
        entry_name.pack(pady=1)
        if existing:
            entry_name.insert(0, existing[0])

        label_amount = ctk.CTkLabel(popup, text="Amount:")
        label_amount.pack(pady=1)
        entry_amount = ctk.CTkEntry(popup)
        entry_amount.pack(pady=1)
        if existing:
            entry_amount.insert(0, str(existing[0]))

        label_freq = ctk.CTkLabel(popup, text="Frequency:")
        label_freq.pack(pady=1)
        freq_var = ctk.StringVar(value=existing[1] if existing else "Monthly")
        freq_menu = ctk.CTkOptionMenu(popup, variable=freq_var, values=["Weekly", "Biweekly", "Monthly"])
        freq_menu.pack(pady=1)

        start_date_var = ctk.StringVar(value=existing[2] if existing else "Not set")
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
        start_date_label = ctk.CTkLabel(popup, text=f"Start Date: {start_date_var.get()}")
        start_date_label.pack(pady=1)

        error_label = ctk.CTkLabel(popup, text="", text_color="red")
        error_label.pack(pady=5)

        def submit():
            try:
                name = entry_name.get()
                amount = float(entry_amount.get())
                freq = freq_var.get()
                start_date = start_date_var.get()
                if start_date == "Not set":
                    error_label.configure(text="Please pick a start date.")
                    return
                item = (name, amount, freq, start_date)
                if existing and index is not None:
                    item_list[index] = item
                else:
                    item_list.append(item)
                self.update_recurring_items_display(
                    item_list,
                    display_label,
                    lambda idx: self.on_recurring_item_click(
                        item_list,
                        display_label,
                        title.replace("Add", "Edit"),
                        idx
                    )
                )
                popup.destroy()
            except ValueError:
                error_label.configure(text="Please enter a valid amount.")

        submit_btn = ctk.CTkButton(popup, text="Save", command=submit)
        submit_btn.pack(pady=1)

        popup.update()
        popup.grab_set()

    def update_recurring_items_display(self, item_list, display_frame, on_item_click):
        # Clear previous widgets
        for widget in display_frame.winfo_children():
            widget.destroy()
        if not item_list:
            label = ctk.CTkLabel(display_frame, text="No items")
            label.pack()
        else:
            for idx, (name, amt, freq, date) in enumerate(item_list):
                btn = ctk.CTkButton(
                    display_frame,
                    text=f"{name}: ${amt:.2f} - {freq} - {date}",
                    command=lambda i=idx: on_item_click(i),
                    fg_color="transparent",
                    text_color="black",
                    hover_color="#e0e0e0",
                    anchor="w"
                )
                btn.pack(fill="x", padx=2, pady=1)

    def on_recurring_item_click(self, item_list, display_frame, title, index):
        existing = item_list[index]
        self.add_or_edit_recurring_item(
            item_list,
            display_frame,
            title,
            existing,
            index
        )

    def save_data(self):
        data = {
            "current_balance": self.current_balance,
            "target_date": self.target_label.cget("text").replace("Target Date: ", ""),
            "recurring_income": [
                {"name": name, "amount": amt, "frequency": freq, "start_date": date}
                for name, amt, freq, date in self.recurring_income_list
            ],
            "recurring_expenses": [
                {"name": name, "amount": amt, "frequency": freq, "start_date": date}
                for name, amt, freq, date in self.recurring_expenses_list
            ]
        }
        try:
            with open("financial_data.json", "w") as f:
                json.dump(data, f, indent=4)
            print("Data saved to financial_data.json")
        except Exception as e:
            print(f"Error saving data: {e}")
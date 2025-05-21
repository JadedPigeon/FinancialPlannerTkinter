import customtkinter as ctk

class MainWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.navbar = NavBar(self, controller=self)
        self.navbar.pack(side="left", fill="y")

        self.action_window = ActionWindow(self, controller=self)
        self.action_window.pack(side="right", fill="both", expand=True)

class NavBar(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Example content for NavBar
        label = ctk.CTkLabel(self, text="Navigation Bar")
        label.pack(padx=10, pady=10)

class ActionWindow(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Example content for ActionWindow
        label = ctk.CTkLabel(self, text="Action Window")
        label.pack(padx=10, pady=10)
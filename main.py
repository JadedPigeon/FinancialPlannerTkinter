import customtkinter as ctk
from ui.main_window import NavBar, ActionWindow, MainWindow

def main():
    root = ctk.CTk()
    root.title("Python Financial Planner")
    root.geometry("800x600")  # You can adjust this to fit your layout

    app = MainWindow(root)

    app.mainloop()

if __name__ == "__main__":
    main()
"""
Employee Management System
--------------------------
Run this file to launch the application.
    python main.py
"""

from Dbconnection import initialize_database
from gui import EmployeeApp

if __name__ == "__main__":
    # Step 1: Create DB and table if not exist
    ok, msg = initialize_database()
    if not ok:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Startup Error", msg)
        root.destroy()
    else:
        # Step 2: Launch GUI
        app = EmployeeApp()
        app.mainloop()
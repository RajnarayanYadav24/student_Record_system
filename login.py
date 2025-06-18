import tkinter as tk
from tkinter import messagebox
import student_gui  # This is your main app module

def check_login():
    username = user_entry.get()
    password = pass_entry.get()
    if username == 'admin' and password == 'admin123':
        login_window.destroy()
        student_gui.launch_app()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x150")

tk.Label(login_window, text="Username").pack(pady=5)
user_entry = tk.Entry(login_window)
user_entry.pack()

tk.Label(login_window, text="Password").pack(pady=5)
pass_entry = tk.Entry(login_window, show="*")
pass_entry.pack()

tk.Button(login_window, text="Login", command=check_login).pack(pady=10)

login_window.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import pandas as pd

FILENAME = "students.csv"

# Ensure file exists
if not os.path.exists(FILENAME):
    with open(FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Roll', 'Name', 'Marks'])

def validate_marks(marks):
    return marks.isdigit()

def add_student():
    roll, name, marks = roll_entry.get(), name_entry.get(), marks_entry.get()
    if not (roll and name and marks):
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    if not validate_marks(marks):
        messagebox.showwarning("Validation Error", "Marks must be numeric.")
        return

    with open(FILENAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([roll, name, marks])

    messagebox.showinfo("Success", "Student added successfully!")
    clear_fields()
    view_all()

def view_all(sort_by=None):
    output_text.delete('1.0', tk.END)
    with open(FILENAME, 'r') as f:
        reader = list(csv.reader(f))
        header = reader[0]
        data = reader[1:]

    if sort_by == "Name":
        data.sort(key=lambda x: x[1])
    elif sort_by == "Marks":
        data.sort(key=lambda x: int(x[2]))

    for row in data:
        output_text.insert(tk.END, f"Roll: {row[0]}, Name: {row[1]}, Marks: {row[2]}\n")

def search_student():
    roll = roll_entry.get()
    found = False
    output_text.delete('1.0', tk.END)
    with open(FILENAME, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == roll:
                output_text.insert(tk.END, f"Roll: {row[0]}, Name: {row[1]}, Marks: {row[2]}\n")
                found = True
                break
    if not found:
        messagebox.showinfo("Not Found", "No student with that roll number.")

def update_student():
    roll, name, marks = roll_entry.get(), name_entry.get(), marks_entry.get()
    if not validate_marks(marks):
        messagebox.showwarning("Validation Error", "Marks must be numeric.")
        return
    updated = False
    rows = []
    with open(FILENAME, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == roll:
                rows.append([roll, name, marks])
                updated = True
            else:
                rows.append(row)

    if updated:
        with open(FILENAME, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        messagebox.showinfo("Updated", "Record updated successfully.")
    else:
        messagebox.showinfo("Not Found", "Student not found.")
    view_all()

def delete_student():
    roll = roll_entry.get()
    deleted = False
    rows = []
    with open(FILENAME, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != roll:
                rows.append(row)
            else:
                deleted = True
    if deleted:
        with open(FILENAME, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        messagebox.showinfo("Deleted", "Record deleted.")
    else:
        messagebox.showinfo("Not Found", "Roll number not found.")
    view_all()

def export_to_excel():
    df = pd.read_csv(FILENAME)
    df.to_excel("students.xlsx", index=False)
    messagebox.showinfo("Exported", "Data exported to students.xlsx")

def clear_fields():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

def sort_records(event):
    selected = sort_option.get()
    view_all(sort_by=selected)

# GUI Setup
def launch_app():
    global root, roll_entry, name_entry, marks_entry, output_text, sort_option
    root = tk.Tk()
    root.title("Student Record System")
    root.geometry("650x550")

    tk.Label(root, text="Roll No").grid(row=0, column=0)
    tk.Label(root, text="Name").grid(row=1, column=0)
    tk.Label(root, text="Marks").grid(row=2, column=0)

    roll_entry = tk.Entry(root)
    name_entry = tk.Entry(root)
    marks_entry = tk.Entry(root)

    roll_entry.grid(row=0, column=1, padx=10, pady=5)
    name_entry.grid(row=1, column=1, padx=10, pady=5)
    marks_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(root, text="Add", width=12, command=add_student).grid(row=3, column=0, pady=10)
    tk.Button(root, text="Search", width=12, command=search_student).grid(row=3, column=1)
    tk.Button(root, text="Update", width=12, command=update_student).grid(row=4, column=0)
    tk.Button(root, text="Delete", width=12, command=delete_student).grid(row=4, column=1)
    tk.Button(root, text="Export to Excel", width=15, command=export_to_excel).grid(row=5, column=0)
    tk.Button(root, text="Clear", width=12, command=clear_fields).grid(row=5, column=1)

    tk.Label(root, text="Sort By:").grid(row=6, column=0, pady=5)
    sort_option = ttk.Combobox(root, values=["Name", "Marks"])
    sort_option.grid(row=6, column=1)
    sort_option.bind("<<ComboboxSelected>>", sort_records)

    output_text = tk.Text(root, width=80, height=15)
    output_text.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    view_all()
    root.mainloop()

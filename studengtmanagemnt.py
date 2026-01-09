import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import time

# Connect to MySQL Database
db = mysql.connector.connect(
    host="localhost",
    user="project",
    password="ritin150",
    database="school_db"
)
cursor = db.cursor()

# Fetch student IDs for dropdown
def fetch_student_ids():
    cursor.execute("SELECT id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    return student_ids

# Fetch all students data
def fetch_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    student_table.delete(*student_table.get_children())  # Clear existing data
    for row in rows:
        student_table.insert("", tk.END, values=row)

# Fetch all marks data
def fetch_marks():
    student_id = marks_student_id_dropdown.get()
    if student_id:
        cursor.execute("SELECT subject, marks FROM marks WHERE student_id=%s", (student_id,))
        rows = cursor.fetchall()
        marks_table.delete(*marks_table.get_children())  # Clear existing data
        for row in rows:
            marks_table.insert("", tk.END, values=row)
    else:
        messagebox.showerror("Error", "Select a student ID!")

# Fetch all attendance data
def fetch_attendance():
    student_id = attendance_student_id_dropdown.get()
    if student_id:
        cursor.execute("SELECT date, status FROM attendance WHERE student_id=%s", (student_id,))
        rows = cursor.fetchall()
        attendance_table.delete(*attendance_table.get_children())  # Clear existing data
        for row in rows:
            attendance_table.insert("", tk.END, values=row)
    else:
        messagebox.showerror("Error", "Select a student ID!")

# Insert new student into database
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    student_class = class_entry.get()
    
    if name and age and student_class:
        cursor.execute("INSERT INTO students (name, age, student_class) VALUES (%s, %s, %s)", (name, age, student_class))
        db.commit()
        fetch_students()  # Refresh the student list
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        class_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "All fields must be filled!")

# Insert marks for student
def add_marks():
    student_id = marks_student_id_dropdown.get()
    subject = subject_entry.get()
    marks = marks_entry.get()
    
    if student_id and subject and marks:
        cursor.execute("INSERT INTO marks (student_id, subject, marks) VALUES (%s, %s, %s)", (student_id, subject, marks))
        db.commit()
        fetch_marks()  # Refresh marks for the selected student
        subject_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "All fields must be filled!")

# Insert attendance for student
def add_attendance():
    student_id = attendance_student_id_dropdown.get()
    date = attendance_date_entry.get()
    status = attendance_status.get()
    
    if student_id and date and status:
        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)", (student_id, date, status))
        db.commit()
        fetch_attendance()  # Refresh attendance for the selected student
        attendance_date_entry.delete(0, tk.END)
        attendance_status.set('')  # Reset dropdown
    else:
        messagebox.showerror("Error", "All fields must be filled!")

# Update Dropdowns
def update_dropdown():
    student_ids = fetch_student_ids()
    if student_ids:  # Check if there are student IDs
        student_id_dropdown['values'] = student_ids
        marks_student_id_dropdown['values'] = student_ids
        attendance_student_id_dropdown['values'] = student_ids
        roll_no_dropdown['values'] = student_ids
    else:
        print("No student data available.")

# Function to update the subject dropdown based on the selected roll number
def update_subject_dropdown(event):
    student_id = roll_no_dropdown.get()
    if student_id:
        subjects = fetch_subjects(student_id)
        subject_dropdown['values'] = subjects
        subject_dropdown.set('')  # Reset the subject dropdown

# Function to fetch subjects based on the student ID
def fetch_subjects(student_id):
    cursor.execute("SELECT subject FROM marks WHERE student_id=%s", (student_id,))
    subjects = [row[0] for row in cursor.fetchall()]
    return subjects

# Function to update marks in the database
def update_marks():
    student_id = roll_no_dropdown.get()
    subject = subject_dropdown.get()
    marks = new_marks_entry.get()
    
    if student_id and subject and marks:
        cursor.execute("UPDATE marks SET marks=%s WHERE student_id=%s AND subject=%s", (marks, student_id, subject))
        db.commit()
        fetch_marks()  # Refresh marks for the selected student
        new_marks_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Marks updated successfully!")
    else:
        messagebox.showerror("Error", "All fields must be filled!")

# Main Window Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("1000x700")

# Create Frames
dashboard = tk.Frame(root)
student_section = tk.Frame(root)
marks_section = tk.Frame(root)
attendance_section = tk.Frame(root)
update_section = tk.Frame(root)

for frame in (dashboard, student_section, marks_section, attendance_section, update_section):
    frame.grid(row=0, column=0, sticky="nsew")

# **Dashboard UI**
tk.Label(dashboard, text="Student Management System", font=("Arial", 18)).pack(pady=20)
tk.Button(dashboard, text="Student Section", command=lambda: show_frame(student_section), width=20).pack(pady=5)
tk.Button(dashboard, text="Marks Section", command=lambda: show_frame(marks_section), width=20).pack(pady=5)
tk.Button(dashboard, text="Attendance Section", command=lambda: show_frame(attendance_section), width=20).pack(pady=5)
tk.Button(dashboard, text="Update Section", command=lambda: show_frame(update_section), width=20).pack(pady=5)

clock_label = tk.Label(dashboard, font=("Arial", 14))
clock_label.pack(pady=10)

# **Student Section UI**
tk.Label(student_section, text="Student Section", font=("Arial", 16)).pack(pady=10)

# Fields for adding student
tk.Label(student_section, text="Name").pack()
name_entry = tk.Entry(student_section)
name_entry.pack(pady=5)

tk.Label(student_section, text="Age").pack()
age_entry = tk.Entry(student_section)
age_entry.pack(pady=5)

tk.Label(student_section, text="Class").pack()
class_entry = tk.Entry(student_section)
class_entry.pack(pady=5)

tk.Button(student_section, text="Add Student", command=add_student).pack(pady=5)
tk.Button(student_section, text="Fetch Students", command=fetch_students).pack(pady=5)

student_id_dropdown = ttk.Combobox(student_section, state="readonly")
student_id_dropdown.pack(pady=5)

# Create Treeview for displaying students
student_table = ttk.Treeview(student_section, columns=("ID", "Name", "Age", "Class"), show="headings")
student_table.heading("ID", text="ID")
student_table.heading("Name", text="Name")
student_table.heading("Age", text="Age")
student_table.heading("Class", text="Class")
student_table.pack(pady=10, fill="both", expand=True)

tk.Button(student_section, text="Back", command=lambda: show_frame(dashboard)).pack(pady=10)

# **Marks Section UI**
tk.Label(marks_section, text="Marks Section", font=("Arial", 16)).pack(pady=10)

# Fields for adding marks
marks_student_id_dropdown = ttk.Combobox(marks_section, state="readonly")
marks_student_id_dropdown.pack(pady=5)

tk.Label(marks_section, text="Subject").pack()
subject_entry = tk.Entry(marks_section)
subject_entry.pack(pady=5)

tk.Label(marks_section, text="Marks").pack()
marks_entry = tk.Entry(marks_section)
marks_entry.pack(pady=5)

tk.Button(marks_section, text="Add Marks", command=add_marks).pack(pady=5)
tk.Button(marks_section, text="Fetch Marks", command=fetch_marks).pack(pady=5)

# Create Treeview for displaying marks
marks_table = ttk.Treeview(marks_section, columns=("Subject", "Marks"), show="headings")
marks_table.heading("Subject", text="Subject")
marks_table.heading("Marks", text="Marks")
marks_table.pack(pady=10, fill="both", expand=True)

tk.Button(marks_section, text="Back", command=lambda: show_frame(dashboard)).pack(pady=10)

# **Attendance Section UI**
tk.Label(attendance_section, text="Attendance Section", font=("Arial", 16)).pack(pady=10)

# Fields for adding attendance
attendance_student_id_dropdown = ttk.Combobox(attendance_section, state="readonly")
attendance_student_id_dropdown.pack(pady=5)

tk.Label(attendance_section, text="Date (YYYY-MM-DD)").pack()
attendance_date_entry = tk.Entry(attendance_section)
attendance_date_entry.pack(pady=5)

tk.Label(attendance_section, text="Status").pack()
attendance_status = ttk.Combobox(attendance_section, values=["Present", "Absent"], state="readonly")
attendance_status.pack(pady=5)

tk.Button(attendance_section, text="Add Attendance", command=add_attendance).pack(pady=5)
tk.Button(attendance_section, text="Fetch Attendance", command=fetch_attendance).pack(pady=5)

# Create Treeview for displaying attendance
attendance_table = ttk.Treeview(attendance_section, columns=("Date", "Status"), show="headings")
attendance_table.heading("Date", text="Date")
attendance_table.heading("Status", text="Status")
attendance_table.pack(pady=10, fill="both", expand=True)

tk.Button(attendance_section, text="Back", command=lambda: show_frame(dashboard)).pack(pady=10)

# **Update Section UI**
tk.Label(update_section, text="Update Marks", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=20)

# Roll Number Dropdown (populated with student IDs)
tk.Label(update_section, text="Roll No").grid(row=1, column=0)
roll_no_dropdown = ttk.Combobox(update_section, state="readonly")
roll_no_dropdown.grid(row=1, column=1)

# Subject Dropdown (populated dynamically based on the selected Roll No)
tk.Label(update_section, text="Subject").grid(row=2, column=0)
subject_dropdown = ttk.Combobox(update_section, state="readonly")
subject_dropdown.grid(row=2, column=1)

# Entry field for new marks
tk.Label(update_section, text="New Marks").grid(row=3, column=0)
new_marks_entry = tk.Entry(update_section)
new_marks_entry.grid(row=3, column=1)

# Button to update marks
tk.Button(update_section, text="Update", command=update_marks).grid(row=4, column=0, columnspan=2, pady=10)

# Button to go back to dashboard
tk.Button(update_section, text="Back", command=lambda: show_frame(dashboard)).grid(row=5, column=0, columnspan=2, pady=10)

# Bind event to update subject dropdown when roll number is selected
roll_no_dropdown.bind("<<ComboboxSelected>>", update_subject_dropdown)

# Start with dashboard visible
def show_frame(frame):
    frame.tkraise()

# Initial setup to populate dropdowns
update_dropdown()

# Start the GUI
root.mainloop()

import sqlite3
import ttkbootstrap as tb
from ttkbootstrap.constants import SUCCESS, INFO, WARNING, DANGER
from tkinter import messagebox
from datetime import datetime, timedelta
from tkinter import ttk
import winsound

# Database Setup
conn = sqlite3.connect('gym_attendance.db')
cursor = conn.cursor()

# Ensure the database tables exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS members (
        roll_no TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT,
        dob TEXT,
        start_date TEXT,
        end_date TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        roll_no TEXT,
        name TEXT,
        date TEXT,
        status TEXT,
        FOREIGN KEY(roll_no) REFERENCES members(roll_no)
    )
''')
conn.commit()

# Functions
def play_sound(frequency=750, duration=300):
    winsound.Beep(frequency, duration)

def mark_attendance(event=None):
    roll_no = entry_roll.get().strip()
    date = datetime.now().strftime("%Y-%m-%d")

    if not roll_no:
        messagebox.showwarning("Input Error", "Please enter Roll Number.")
        return

    # Check if attendance already marked for today
    cursor.execute('SELECT * FROM attendance WHERE roll_no = ? AND date = ?', (roll_no, date))
    if cursor.fetchone():
        messagebox.showinfo("Already Marked", "Attendance already marked for today!")
        return

    cursor.execute('SELECT end_date, name FROM members WHERE roll_no = ?', (roll_no,))
    result = cursor.fetchone()

    if result:
        end_date = datetime.strptime(result[0], "%Y-%m-%d")
        today = datetime.now()

        if today.date() > end_date.date():
            messagebox.showerror("Subscription Expired", "Your subscription has ended!")
            play_sound(frequency=1000, duration=500)
        else:
            try:
                cursor.execute('INSERT INTO attendance (roll_no, name, date, status) VALUES (?, ?, ?, ?)',
                               (roll_no, result[1], date, "Present"))
                conn.commit()
                messagebox.showinfo("Success", f"Attendance marked for Roll No {roll_no}")
                play_sound()
                # Clear the text box only after successful insertion
                entry_roll.delete(0, tb.END)
                entry_roll.focus_set()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to mark attendance: {e}")
    else:
        messagebox.showwarning("Error", "Member not found!")
        entry_roll.delete(0, tb.END)
        entry_roll.focus_set()

def add_member():
    roll_no = entry_roll_add.get().strip()
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    dob = entry_dob.get().strip()
    start_date = entry_start.get().strip()
    end_date = entry_end.get().strip()

    if not all([roll_no, name, phone, dob, start_date, end_date]):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        dob = datetime.strptime(dob, "%d %m %Y").strftime("%Y-%m-%d")
        start_date = datetime.strptime(start_date, "%d %m %Y").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%d %m %Y").strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Date Error", "Dates must be in DD MM YYYY format.")
        return

    try:
        cursor.execute('INSERT INTO members VALUES (?, ?, ?, ?, ?, ?)',
                       (roll_no, name, phone, dob, start_date, end_date))
        conn.commit()
        messagebox.showinfo("Success", "Member added successfully!")
        # Clear all fields only after successful insertion
        clear_entries()
        entry_roll_add.focus_set()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll Number already exists!")


def view_members():
    for widget in view_frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(view_frame, columns=("Roll No", "Name", "Phone", "DOB", "Start Date", "End Date"), show='headings')
    for col in ("Roll No", "Name", "Phone", "DOB", "Start Date", "End Date"):
        tree.heading(col, text=col)
        tree.column(col, width=100)  # Set column width
    
    scrollbar = ttk.Scrollbar(view_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tb.END, values=row)

    view_frame.pack(expand=True, fill='both', pady=10)

def view_today_attendance():
    today = datetime.now().strftime("%Y-%m-%d")
    
    attendance_window = tb.Toplevel(root)
    attendance_window.title("Today's Attendance")
    attendance_window.geometry("600x400")

    frame = tb.Frame(attendance_window)
    frame.pack(fill='both', expand=True)

    tree = ttk.Treeview(frame, columns=("Roll No", "Name", "Date", "Status"), show='headings')
    for col in ("Roll No", "Name", "Date", "Status"):
        tree.heading(col, text=col)
        tree.column(col, width=150)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    cursor.execute("SELECT roll_no, name, date, status FROM attendance WHERE date = ?", (today,))
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tb.END, values=row)

def view_expiring_subscriptions():
    today = datetime.now().date()
    expiring_date = today + timedelta(days=3)

    expiring_window = tb.Toplevel(root)
    expiring_window.title("Expiring Subscriptions")
    expiring_window.geometry("600x400")

    frame = tb.Frame(expiring_window)
    frame.pack(fill='both', expand=True)

    tree = ttk.Treeview(frame, columns=("Roll No", "Name", "End Date", "Days Left"), show='headings')
    for col in ("Roll No", "Name", "End Date", "Days Left"):
        tree.heading(col, text=col)
        tree.column(col, width=150)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    cursor.execute("SELECT roll_no, name, end_date FROM members")
    rows = cursor.fetchall()
    for row in rows:
        end_date = datetime.strptime(row[2], "%Y-%m-%d").date()
        days_left = (end_date - today).days
        if 0 <= days_left <= 3:
            tree.insert("", tb.END, values=(row[0], row[1], row[2], f"{days_left} days"))

def clear_entries():
    entry_roll_add.delete(0, tb.END)
    entry_name.delete(0, tb.END)
    entry_phone.delete(0, tb.END)
    entry_dob.delete(0, tb.END)
    entry_start.delete(0, tb.END)
    entry_end.delete(0, tb.END)

# GUI Setup
root = tb.Window(themename="superhero")
root.title("Gym Attendance System")
root.geometry("800x900")

# Title
title_label = tb.Label(root, text="Gym Attendance System", font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

# Mark Attendance Section
frame_attendance = tb.Frame(root)
frame_attendance.pack(pady=10)

tb.Label(frame_attendance, text="Enter Roll Number:", font=("Helvetica", 14)).grid(row=0, column=0, padx=10)
entry_roll = tb.Entry(frame_attendance, font=("Helvetica", 14))
entry_roll.grid(row=0, column=1)
entry_roll.bind("<Return>", mark_attendance)

btn_mark = tb.Button(frame_attendance, text="Mark Attendance", command=mark_attendance, bootstyle=SUCCESS)
btn_mark.grid(row=1, column=0, columnspan=2, pady=10)

# Add Member Section
frame_add = tb.LabelFrame(root, text="Add New Member", bootstyle="primary")
frame_add.pack(pady=10, padx=10, fill="x")

fields = [("Roll Number:", "entry_roll_add"), ("Name:", "entry_name"), ("Phone Number:", "entry_phone"),
          ("Date of Birth (DD MM YYYY):", "entry_dob"), 
          ("Start Date (DD MM YYYY):", "entry_start"), 
          ("End Date (DD MM YYYY):", "entry_end")]

entries = {}
for i, (label_text, var_name) in enumerate(fields):
    tb.Label(frame_add, text=label_text, font=("Helvetica", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
    entries[var_name] = tb.Entry(frame_add, font=("Helvetica", 12))
    entries[var_name].grid(row=i, column=1, pady=5, padx=10, sticky="ew")

frame_add.grid_columnconfigure(1, weight=1)

entry_roll_add, entry_name, entry_phone, entry_dob, entry_start, entry_end = [entries[var_name] for _, var_name in fields]

btn_add = tb.Button(frame_add, text="Add Member", command=add_member, bootstyle=INFO)
btn_add.grid(row=len(fields), column=0, columnspan=2, pady=10)

# View Frame for Members
view_frame = tb.Frame(root)

# Report Buttons
btn_frame = tb.Frame(root)
btn_frame.pack(pady=5)

btn_view_members = tb.Button(btn_frame, text="View Members", command=view_members, bootstyle=INFO)
btn_view_members.pack(side='left', padx=5)

btn_view_attendance = tb.Button(btn_frame, text="View Today's Attendance", command=view_today_attendance, bootstyle=WARNING)
btn_view_attendance.pack(side='left', padx=5)

btn_view_expiring = tb.Button(btn_frame, text="View Expiring Subscriptions", command=view_expiring_subscriptions, bootstyle=DANGER)
btn_view_expiring.pack(side='left', padx=5)

root.mainloop()
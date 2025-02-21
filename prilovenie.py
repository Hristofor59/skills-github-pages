import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

# Global variables
users = {}
verification_codes = {}
logged_in_email = None
logged_in_name = None
password_manager = {}

# Centering function
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width / 2)
    y_coordinate = (screen_height / 2) - (height / 2)
    window.geometry(f"{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)}")

# Function to switch frames
def switch_to_frame(frame):
    for f in (login_frame, register_frame, verification_frame, dashboard_frame, password_manager_frame):
        f.pack_forget()
    frame.pack()

# Registration function
def register():
    name = name_register_entry.get()
    email = email_register_entry.get()
    password = password_register_entry.get()
    
    if not name or not email or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    if len(password) < 10 or not password.isalnum():
        messagebox.showerror("Error", "Password must be at least 10 characters long and contain only letters and digits.")
        return
    
    if email in users:
        messagebox.showerror("Error", "This email is already registered!")
        return
    
    users[email] = {"name": name, "password": password}
    messagebox.showinfo("Success", "Registration successful!")
    switch_to_frame(login_frame)

# Login function
def login():
    global logged_in_email, logged_in_name
    email = email_login_entry.get()
    password = password_login_entry.get()
    
    if email not in users or users[email]["password"] != password:
        messagebox.showerror("Error", "Invalid email or password!")
        return
    
    verification_code = str(random.randint(100000, 999999))
    verification_codes[email] = verification_code
    messagebox.showinfo("2FA Code", f"Your verification code is: {verification_code}")
    logged_in_email = email
    logged_in_name = users[email]["name"]
    switch_to_frame(verification_frame)

# Verify function
def verify_code():
    global logged_in_name
    code = verification_code_entry.get()
    
    if logged_in_email in verification_codes and verification_codes[logged_in_email] == code:
        messagebox.showinfo("Success", "Login successful!")
        welcome_label.config(text=f"Welcome, {logged_in_name}!")
        switch_to_frame(dashboard_frame)
    else:
        messagebox.showerror("Error", "Invalid verification code!")

# Show password function
def toggle_password():
    if password_login_entry.cget('show') == "*":
        password_login_entry.config(show="")
        show_password_button.config(text="Hide Password")
    else:
        password_login_entry.config(show="*")
        show_password_button.config(text="Show Password")

# Manage password function
def manage_passwords():
    email = email_manager_entry.get()
    link = link_manager_entry.get()
    
    if email not in users:
        messagebox.showinfo("Info", "No account found with this email.")
        show_registration_fields()
        return
    else:
        # Hide registration fields and show the password manager table
        if email not in password_manager:
            password_manager[email] = []
        
        password_manager[email].append({"email": email, "link": link, "username": users[email]["name"], "password": users[email]["password"]})
        show_password_table(email)

def show_registration_fields():
    # Show the registration fields if the account doesn't exist
    tk.Label(password_manager_frame, text="Register", font=("Arial", 20, "bold"), fg='#4CAF50').pack(pady=20)
    tk.Label(password_manager_frame, text="Name", fg='#333').pack()
    name_register_entry = tk.Entry(password_manager_frame, width=30, font=("Arial", 14), bg='#f5f5f5', bd=2, relief="solid")
    name_register_entry.pack()
    tk.Label(password_manager_frame, text="Email", fg='#333').pack()
    email_register_entry = tk.Entry(password_manager_frame, width=30, font=("Arial", 14), bg='#f5f5f5', bd=2, relief="solid")
    email_register_entry.pack()
    tk.Label(password_manager_frame, text="Password", fg='#333').pack()
    password_register_entry = tk.Entry(password_manager_frame, width=30, font=("Arial", 14), show="*", bg='#f5f5f5', bd=2, relief="solid")
    password_register_entry.pack()
    register_button = tk.Button(password_manager_frame, text="Register", command=register, bg='#4CAF50', fg='white', font=("Arial", 14), relief="flat")
    register_button.pack(pady=10)

# Show password table
def show_password_table(email):
    # Clear previous widgets
    for widget in password_manager_frame.winfo_children():
        widget.destroy()

    if email in password_manager:
        # Display greeting with username
        username = users[email]["name"]
        tk.Label(password_manager_frame, text=f"Здравей, {username}", font=("Arial", 20, "bold"), fg='#4CAF50').pack(pady=20)

        # Create a table for the links and data
        columns = ("Email", "Username", "Password", "Link")
        tree = ttk.Treeview(password_manager_frame, columns=columns, show="headings", height=10)  # Increased height
        tree.pack(pady=20)

        for col in columns:
            tree.heading(col, text=col, anchor=tk.W)
            tree.column(col, width=150, anchor=tk.W)  # Increased column width

        # Add a scrollbar to the table
        scrollbar = ttk.Scrollbar(password_manager_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        for entry in password_manager[email]:
            tree.insert("", "end", values=(entry["email"], entry["username"], entry["password"], entry["link"]))

# Tkinter main window
root = tk.Tk()
root.title("Modern Authentication App")
center_window(root, 600, 600)
root.configure(bg='#f5f5f5')

# Frames
login_frame = tk.Frame(root, bg='#f5f5f5')
register_frame = tk.Frame(root, bg='#f5f5f5')
verification_frame = tk.Frame(root, bg='#f5f5f5')
dashboard_frame = tk.Frame(root, bg='#f5f5f5')
password_manager_frame = tk.Frame(root, bg='#f5f5f5')

# Login form
tk.Label(login_frame, text="Login", font=("Arial", 30, "bold"), fg='#4CAF50').pack(pady=20)
tk.Label(login_frame, text="Email", fg='#333').pack()
email_login_entry = tk.Entry(login_frame, width=30, font=("Arial", 14), bg='#f5f5f5', bd=2, relief="solid")
email_login_entry.pack()
tk.Label(login_frame, text="Password", fg='#333').pack()
password_login_entry = tk.Entry(login_frame, width=30, font=("Arial", 14), show="*", bg='#f5f5f5', bd=2, relief="solid")
password_login_entry.pack()
login_button = tk.Button(login_frame, text="Login", command=login, bg='#4CAF50', fg='white', font=("Arial", 14), relief="flat")
login_button.pack(pady=10)
show_password_button = tk.Button(login_frame, text="Show Password", command=toggle_password, bg='#4CAF50', fg='white', font=("Arial", 14), relief="flat")
show_password_button.pack(pady=10)
register_button = tk.Button(login_frame, text="Register", command=lambda: switch_to_frame(register_frame), bg='#ffffff', fg='#4CAF50', font=("Arial", 14), relief="flat")
register_button.pack()

# Registration form
tk.Label(register_frame, text="Register", font=("Arial", 30, "bold"), fg='#4CAF50').pack(pady=20)
tk.Label(register_frame, text="Name", fg='#333').pack()
name_register_entry = tk.Entry(register_frame, width=30, font=("Arial", 14), bg='#f5f5f5', bd=2, relief="solid")
name_register_entry.pack()
tk.Label(register_frame, text="Email", fg='#333').pack()
email_register_entry = tk.Entry(register_frame, width=30, font=("Arial", 14), bg='#f5f5f5', bd=2, relief="solid")
email_register_entry.pack()
tk.Label(register_frame, text="Password", fg='#333').pack()
password_register_entry = tk.Entry(register_frame, width=30, font=("Arial", 14), show="*", bg='#f5f5f5', bd=2, relief="solid")
password_register_entry.pack()
register_button = tk.Button(register_frame, text="Register", command=register, bg='#4CAF50', fg='white', font=("Arial", 14), relief="flat")
register_button.pack(pady=10)
back_button = tk.Button(register_frame, text="Back to Login", command=lambda: switch_to_frame(login_frame), bg='white', fg='black', font=("Arial", 14), relief="flat")
back_button.pack()

# Verification form
tk.Label(verification_frame, text="Enter Verification Code", font=("Arial", 20, "bold"), fg='#4CAF50').pack(pady=20)
verification_code_entry = tk.Entry(verification_frame, width=30, font=("Arial", 14), bg='#f5f5f5', bd=2, relief="solid")
verification_code_entry.pack()
verify_button = tk.Button(verification_frame, text="Verify", command=verify_code, bg='#4CAF50', fg='white', font=("Arial", 14), relief="flat")
verify_button.pack(pady=10)

# Dashboard
dashboard_frame.pack()
welcome_label = tk.Label(dashboard_frame, text="", font=("Arial", 20, "bold"), fg='#4CAF50')
welcome_label.pack(pady=20)
manager_button = tk.Button(dashboard_frame, text="Password Manager", command=lambda: switch_to_frame(password_manager_frame), bg='#4CAF50', fg='white', font=("Arial", 14), relief="flat")
manager_button.pack(pady=10)
logout_button = tk.Button(dashboard_frame, text="Logout", command=lambda: switch_to_frame(login_frame), bg='white', fg='black', font=("Arial", 14), relief="flat")
logout_button.pack()

# Password manager form
tk.Label(password_manager_frame, text="Password Manager", font=("Arial", 30, "bold"), fg='#4CAF50').pack(pady=20)
tk.Label(password_manager_frame, text="Enter Email", fg='#333').pack()
email_manager_entry = tk.Entry(password_manager_frame, width=30, font=("Arial", 14), bg='#f5f5f5', bd=2, relief="solid")
email_manager_entry.pack(pady=10)
tk.Label(password_manager_frame, text="Enter Link", fg='#333').pack()
link_manager_entry = tk.Entry(password_manager_frame, width=30, font=("Arial", 14), bg='#f5f5f5', bd=2, relief="solid")
link_manager_entry.pack(pady=10)
manager_button_action = tk.Button(password_manager_frame, text="Manage Passwords", command=manage_passwords, bg='#4CAF50', fg='white', font=("Arial", 14), relief="flat")
manager_button_action.pack(pady=10)

# Start application
switch_to_frame(login_frame)
root.mainloop()

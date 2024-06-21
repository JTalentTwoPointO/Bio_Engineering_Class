import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Donor  # Import your database models

# Database setup
engine = create_engine('sqlite:///becs.db')
Session = sessionmaker(bind=engine)
session = Session()

def submit_donor():
    name = name_entry.get()
    id_number = id_entry.get()
    blood_type = blood_type_combobox.get()
    donation_date = donation_date_entry.get()
    # Add code to save this data to the database
    new_donor = Donor(name=name, id_number=id_number, blood_type=blood_type, donation_date=donation_date)
    session.add(new_donor)
    session.commit()
    print("Donor added successfully!")

# Create the main application window
root = tk.Tk()
root.title("BECS - Blood Donation Entry")

# Create and place labels and entries for data input
tk.Label(root, text="Full Name").grid(row=0, column=0, padx=10, pady=5, sticky='e')
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="ID Number").grid(row=1, column=0, padx=10, pady=5, sticky='e')
id_entry = tk.Entry(root)
id_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Blood Type").grid(row=2, column=0, padx=10, pady=5, sticky='e')
blood_type_combobox = ttk.Combobox(root, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
blood_type_combobox.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Donation Date").grid(row=3, column=0, padx=10, pady=5, sticky='e')
donation_date_entry = tk.Entry(root)
donation_date_entry.grid(row=3, column=1, padx=10, pady=5)

# Create and place the submit button
tk.Button(root, text="Submit", command=submit_donor).grid(row=4, column=0, columnspan=2, pady=10)

# Main loop to run the application
root.mainloop()

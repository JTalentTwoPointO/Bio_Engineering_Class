import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from database_setup import Session, Donor, BloodInventory

session = Session()

# Define the blood compatibility dictionaries
receive_blood_from = {
    "A+": ["A-", "O+", "O-"],
    "O+": ["O-"],
    "B+": ["B-", "O+", "O-"],
    "AB+": ["A+", "B+", "O+", "AB-", "A-", "B-", "O-"],
    "A-": ["O-"],
    "O-": [],
    "B-": ["O-"],
    "AB-": ["A-", "B-", "O-"]
}

donate_blood_to = {
    "A+": ["A+", "AB+"],
    "O+": ["O+", "A+", "B+", "AB+"],
    "B+": ["B+", "AB+"],
    "AB+": ["AB+"],
    "A-": ["A+", "A-", "AB+", "AB-"],
    "O-": ["Everyone"],
    "B-": ["B+", "B-", "AB+", "AB-"],
    "AB-": ["AB+", "AB-"]
}


# Function to submit donor information
def submit_donor():
    name = name_entry.get()
    id_number = id_entry.get()
    blood_type = blood_type_combobox.get()
    donation_date_str = donation_date_entry.get()

    if not name or not id_number or not blood_type or not donation_date_str:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    try:
        donation_date = datetime.strptime(donation_date_str, '%Y-%m-%d').date()
    except ValueError:
        messagebox.showerror("Date Error", "Invalid date format. Please use YYYY-MM-DD.")
        return

    try:
        new_donor = Donor(name=name, id_number=id_number, blood_type=blood_type, donation_date=donation_date)
        session.add(new_donor)

        inventory_entry = session.query(BloodInventory).filter_by(blood_type=blood_type).first()
        if inventory_entry:
            inventory_entry.units += 1
        else:
            inventory_entry = BloodInventory(blood_type=blood_type, units=1)
            session.add(inventory_entry)

        session.commit()
        messagebox.showinfo("Success", "Donor added successfully!")
    except Exception as e:
        session.rollback()
        messagebox.showerror("Database Error", f"An error occurred: {e}")


# Function to view donor entries
def view_entries():
    entries_text.delete(1.0, tk.END)
    try:
        donors = session.query(Donor).all()
        for donor in donors:
            entries_text.insert(tk.END,
                                f"ID: {donor.id}, Name: {donor.name}, ID Number: {donor.id_number}, Blood Type: {donor.blood_type}, Donation Date: {donor.donation_date}\n")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


# Function to check blood availability
def check_availability(blood_type):
    inventory_entry = session.query(BloodInventory).filter_by(blood_type=blood_type).first()
    return inventory_entry.units if inventory_entry else 0


def routine_dispense():
    requested_blood_type = blood_type_combobox_routine.get()
    requested_units = int(units_entry.get())

    available_units = check_availability(requested_blood_type)

    if available_units >= requested_units:
        inventory_entry = session.query(BloodInventory).filter_by(blood_type=requested_blood_type).first()
        inventory_entry.units -= requested_units
        session.commit()
        messagebox.showinfo("Success", f"Dispensed {requested_units} units of {requested_blood_type} blood.")
    else:
        # Get compatible alternatives from the dictionary, excluding the same blood type
        alternatives = receive_blood_from.get(requested_blood_type, [])
        alternative_message = f"Recommended alternative blood types are: {', '.join(alternatives)}" if alternatives else "No alternatives available."

        messagebox.showwarning("Out of Stock",
                               f"Only {available_units} units of {requested_blood_type} available.\n{alternative_message}")

# Function to dispense blood in emergency
def emergency_dispense():
    try:
        inventory_entry = session.query(BloodInventory).filter_by(blood_type="O-").first()
        if inventory_entry and inventory_entry.units > 0:
            inventory_entry.units = 0
            session.commit()
            messagebox.showinfo("Success", "Emergency blood dispensed successfully!")
        else:
            messagebox.showerror("Out of Stock", "O- blood is out of stock.")
    except Exception as e:
        session.rollback()
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        # ToDo - Dispense all O- not just one unit


# Tkinter setup
root = tk.Tk()
root.title("BECS - Blood Donation and Dispensing System")

tab_control = ttk.Notebook(root)

# Donor Entry Tab
donor_entry_tab = ttk.Frame(tab_control)
tab_control.add(donor_entry_tab, text='Donor Entry')

tk.Label(donor_entry_tab, text="Full Name").grid(row=0, column=0, padx=10, pady=5, sticky='e')
name_entry = tk.Entry(donor_entry_tab)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(donor_entry_tab, text="ID Number").grid(row=1, column=0, padx=10, pady=5, sticky='e')
id_entry = tk.Entry(donor_entry_tab)
id_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(donor_entry_tab, text="Blood Type").grid(row=2, column=0, padx=10, pady=5, sticky='e')
blood_type_combobox = ttk.Combobox(donor_entry_tab, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
blood_type_combobox.grid(row=2, column=1, padx=10, pady=5)

tk.Label(donor_entry_tab, text="Donation Date (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5, sticky='e')
donation_date_entry = tk.Entry(donor_entry_tab)
donation_date_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Button(donor_entry_tab, text="Submit", command=submit_donor).grid(row=4, column=0, columnspan=2, pady=10)

entries_text = tk.Text(donor_entry_tab, height=10, width=50)
entries_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

tk.Button(donor_entry_tab, text="View Entries", command=view_entries).grid(row=6, column=0, columnspan=2, pady=10)

# Routine Dispensing Tab
routine_dispensing_tab = ttk.Frame(tab_control)
tab_control.add(routine_dispensing_tab, text='Routine Dispensing')

tk.Label(routine_dispensing_tab, text="Requested Blood Type").grid(row=0, column=0, padx=10, pady=5, sticky='e')
blood_type_combobox_routine = ttk.Combobox(routine_dispensing_tab,
                                           values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
blood_type_combobox_routine.grid(row=0, column=1, padx=10, pady=5)

tk.Label(routine_dispensing_tab, text="Number of Units").grid(row=1, column=0, padx=10, pady=5, sticky='e')
units_entry = tk.Entry(routine_dispensing_tab)
units_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Button(routine_dispensing_tab, text="Dispense Blood", command=routine_dispense).grid(row=2, column=0, columnspan=2,
                                                                                        pady=10)

# Emergency Dispensing Tab
emergency_dispensing_tab = ttk.Frame(tab_control)
tab_control.add(emergency_dispensing_tab, text='Emergency Dispensing')

tk.Button(emergency_dispensing_tab, text="Dispense Emergency Blood (O-)", command=emergency_dispense).grid(row=0,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=10)

tab_control.pack(expand=1, fill='both')

root.mainloop()

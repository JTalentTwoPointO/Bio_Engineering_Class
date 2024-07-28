# gui/donor_entry.py
import json
import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from database import Session, Donor, BloodInventory, AuditLog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class DonorEntry:
    def __init__(self, parent, role):
        self.frame = ttk.Frame(parent)
        self.session = Session()
        self.role = role
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text="Full Name").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.frame, text="ID Number").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.id_entry = tk.Entry(self.frame)
        self.id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.frame, text="Blood Type").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.blood_type_combobox = ttk.Combobox(self.frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        self.blood_type_combobox.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.frame, text="Donation Date (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.donation_date_entry = tk.Entry(self.frame)
        self.donation_date_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.frame, text="Submit", command=self.submit_donor).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.frame, text="Reset", command=self.reset_form).grid(row=5, column=0, columnspan=2, pady=10)
        if self.role == "Admin":
            tk.Button(self.frame, text="Export Data", command=self.export_data).grid(row=6, column=0, columnspan=2,
                                                                                     pady=10)

    def reset_form(self):
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.blood_type_combobox.set('')
        self.donation_date_entry.delete(0, tk.END)

    def submit_donor(self):
        name = self.name_entry.get()
        id_number = self.id_entry.get()
        blood_type = self.blood_type_combobox.get()
        donation_date_str = self.donation_date_entry.get()

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
            self.session.add(new_donor)

            inventory_entry = self.session.query(BloodInventory).filter_by(blood_type=blood_type).first()
            if inventory_entry:
                inventory_entry.units += 1
            else:
                inventory_entry = BloodInventory(blood_type=blood_type, units=1)
                self.session.add(inventory_entry)

            self.session.commit()
            messagebox.showinfo("Success", "Donor added successfully!")
            self.log_activity("Submit Donor", f"Name: {name}, ID: {id_number}, Blood Type: {blood_type}")
            self.reset_form()
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def export_data(self):
        if self.role != "Admin":
            messagebox.showerror("Permission Denied", "Only Admins can export data.")
            return

        data = {
            "donors": [self.serialize(donor) for donor in self.session.query(Donor).all()],
            "inventory": [self.serialize(inventory) for inventory in self.session.query(BloodInventory).all()],
            "logs": [self.serialize(log) for log in self.session.query(AuditLog).all()]
        }

        with open("export_data.json", "w") as f:
            json.dump(data, f, default=str)

        messagebox.showinfo("Export", "Data exported successfully!")
        self.log_activity("Export Data", "Exported data to JSON")

    def log_activity(self, action, details):
        new_log = AuditLog(action=action, details=details)
        self.session.add(new_log)
        self.session.commit()

    def serialize(self, instance):
        return {key: value for key, value in instance.__dict__.items() if key != '_sa_instance_state'}
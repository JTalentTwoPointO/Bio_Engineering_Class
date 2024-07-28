# gui/routine_dispense.py
import tkinter as tk
from tkinter import ttk, messagebox

from database import Session, BloodInventory, AuditLog

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


class RoutineDispense:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.session = Session()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text="Requested Blood Type").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.blood_type_combobox = ttk.Combobox(self.frame, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        self.blood_type_combobox.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.frame, text="Number of Units").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.units_entry = tk.Entry(self.frame)
        self.units_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.frame, text="Dispense Blood", command=self.routine_dispense).grid(row=2, column=0, columnspan=2,
                                                                                         pady=10)

    def routine_dispense(self):
        requested_blood_type = self.blood_type_combobox.get()
        requested_units = int(self.units_entry.get())

        available_units = self.check_availability(requested_blood_type)

        if available_units >= requested_units:
            inventory_entry = self.session.query(BloodInventory).filter_by(blood_type=requested_blood_type).first()
            inventory_entry.units -= requested_units
            self.session.commit()
            messagebox.showinfo("Success", f"Dispensed {requested_units} units of {requested_blood_type} blood.")
            self.log_activity("Routine Dispense", f"Blood Type: {requested_blood_type}, Units: {requested_units}")
        else:
            alternatives = receive_blood_from.get(requested_blood_type, [])
            alternative_message = f"Recommended alternative blood types are: {', '.join(alternatives)}" if alternatives else "No alternatives available."
            messagebox.showwarning("Out of Stock",
                                   f"Only {available_units} units of {requested_blood_type} available.\n{alternative_message}")
            self.log_activity("Routine Dispense Failed",
                              f"Blood Type: {requested_blood_type}, Requested Units: {requested_units}, Available Units: {available_units}")

    def check_availability(self, blood_type):
        inventory_entry = self.session.query(BloodInventory).filter_by(blood_type=blood_type).first()
        return inventory_entry.units if inventory_entry else 0

    def log_activity(self, action, details):
        new_log = AuditLog(action=action, details=details)
        self.session.add(new_log)
        self.session.commit()

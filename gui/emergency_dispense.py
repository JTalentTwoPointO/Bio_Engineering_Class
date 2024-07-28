# gui/emergency_dispense.py
import tkinter as tk
from tkinter import ttk, messagebox

from database import Session, BloodInventory, AuditLog


class EmergencyDispense:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.session = Session()
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.frame, text="Dispense Emergency Blood (O-)", command=self.emergency_dispense).grid(row=0,
                                                                                                          column=0,
                                                                                                          columnspan=2,
                                                                                                          pady=10)

    def emergency_dispense(self):
        try:
            inventory_entry = self.session.query(BloodInventory).filter_by(blood_type="O-").first()
            if inventory_entry and inventory_entry.units > 0:
                inventory_entry.units = 0
                self.session.commit()
                messagebox.showinfo("Success", "Emergency blood dispensed successfully!")
                self.log_activity("Emergency Dispense", "Dispensed O- blood")
            else:
                messagebox.showerror("Out of Stock", "O- blood is out of stock.")
                self.log_activity("Emergency Dispense Failed", "O- blood out of stock")
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def log_activity(self, action, details):
        new_log = AuditLog(action=action, details=details)
        self.session.add(new_log)
        self.session.commit()

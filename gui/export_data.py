import json
import tkinter as tk
from tkinter import messagebox

from database import Session, Donor, BloodInventory, AuditLog


class ExportData:
    def __init__(self, parent):
        self.session = Session()
        tk.Button(parent, text="Export Data", command=self.export_data).pack(pady=10)

    def export_data(self):
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

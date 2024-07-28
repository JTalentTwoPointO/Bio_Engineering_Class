# gui/view_logs.py
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from database import Session, AuditLog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ViewLogs:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.session = Session()
        self.create_widgets()

    def create_widgets(self):
        self.logs_text = tk.Text(self.frame, height=20, width=100)
        self.logs_text.grid(row=0, column=0, padx=10, pady=10)

        tk.Button(self.frame, text="Refresh Logs", command=self.view_logs).grid(row=1, column=0, pady=10)

    def view_logs(self):
        self.logs_text.delete(1.0, tk.END)
        try:
            logs = self.session.query(AuditLog).all()
            for log in logs:
                self.logs_text.insert(tk.END,
                                      f"ID: {log.id}, Timestamp: {log.timestamp}, Action: {log.action}, Details: {log.details}\n")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
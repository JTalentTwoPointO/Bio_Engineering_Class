# gui/main.py
import pickle
import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk, messagebox

import numpy as np

from gui.auth import Auth
from gui.donor_entry import DonorEntry
from gui.emergency_dispense import EmergencyDispense
from gui.routine_dispense import RoutineDispense
from gui.view_logs import ViewLogs

# Load the model
with open('blood_demand_model.pkl', 'rb') as f:
    model = pickle.load(f)


# Predict blood demand
def predict_blood_demand(days_ahead):
    today_numeric = np.array([(date.today() + timedelta(days=days_ahead)).toordinal()]).reshape(-1, 1)
    prediction = model.predict(today_numeric)
    return prediction


class PredictionTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text="Days Ahead").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.days_entry = tk.Entry(self.frame)
        self.days_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self.frame, text="Predict", command=self.predict).grid(row=1, column=0, columnspan=2, pady=10)
        self.result_label = tk.Label(self.frame, text="")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=10)

    def predict(self):
        try:
            days_ahead = int(self.days_entry.get())
            prediction = predict_blood_demand(days_ahead)
            result_text = "Predicted units:\n"
            for i, blood_type in enumerate(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']):
                result_text += f"{blood_type}: {prediction[0][i]:.2f}\n"
            self.result_label.config(text=result_text)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of days.")

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BECS - Blood Donation and Dispensing System")
        self.auth = Auth(root, self.on_login)

    def on_login(self, role):
        self.role = role
        self.tab_control = ttk.Notebook(self.root)

        if role in ["Admin", "User"]:
            donor_entry_tab = DonorEntry(self.tab_control, role)
            self.tab_control.add(donor_entry_tab.frame, text='Donor Entry')

        if role in ["Admin", "User"]:
            routine_dispensing_tab = RoutineDispense(self.tab_control, role)
            self.tab_control.add(routine_dispensing_tab.frame, text='Routine Dispensing')

        if role == "Admin":
            emergency_dispensing_tab = EmergencyDispense(self.tab_control, role)
            self.tab_control.add(emergency_dispensing_tab.frame, text='Emergency Dispensing')

            log_viewing_tab = ViewLogs(self.tab_control)
            self.tab_control.add(log_viewing_tab.frame, text='Audit Logs')

        if role in ["Admin", "User"]:
            prediction_tab = PredictionTab(self.tab_control)
            self.tab_control.add(prediction_tab.frame, text='Predict Blood Demand')

        if self.tab_control.tabs():  # Only pack if there are tabs
            self.tab_control.pack(expand=1, fill='both')
        else:
            messagebox.showinfo("Access Denied", "You do not have permission to access any tabs.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
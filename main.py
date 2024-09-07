# gui/main.py
import pickle
import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk, messagebox

import numpy as np
import pandas as pd

from gui.auth import Auth
from gui.donor_entry import DonorEntry
from gui.emergency_dispense import EmergencyDispense
from gui.routine_dispense import RoutineDispense
from gui.view_logs import ViewLogs


# Predict blood demand
def predict_blood_demand(days_ahead, blood_type):
    try:
        # Load the saved model, label encoder, and scaler
        with open('blood_demand_model.pkl', 'rb') as f:
            saved_data = pickle.load(f)

        model = saved_data['model']
        label_encoder = saved_data['label_encoder']
        scaler = saved_data['scaler']

        # Get today's date in numerical format and add days_ahead
        future_date = date.today() + timedelta(days=days_ahead)
        future_date_numeric = future_date.toordinal()

        # Feature engineering: Get the day of the week and month
        day_of_week = future_date.weekday()
        month = future_date.month

        # Encode the selected blood type
        blood_type_encoded = label_encoder.transform([blood_type])[0]

        # Prepare the input data: date_numeric, day_of_week, month, blood_type_encoded (4 features)
        input_data = np.array([[future_date_numeric, day_of_week, month, blood_type_encoded]])

        # Create DataFrame to match training features
        input_df = pd.DataFrame(input_data, columns=['date_numeric', 'day_of_week', 'month', 'blood_type_encoded'])

        # Normalize the input data using the scaler (only on date, day, and month)
        features_to_scale = ['date_numeric', 'day_of_week', 'month']
        input_df[features_to_scale] = scaler.transform(input_df[features_to_scale])

        # Convert back to NumPy array for prediction
        input_data = input_df.to_numpy()

        # Make the prediction
        prediction = model.predict(input_data)

        return prediction[0]

    except Exception as e:
        print(f"Error during prediction: {e}")
        return None


class PredictionTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.frame, text="Days Ahead").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.days_entry = tk.Entry(self.frame)
        self.days_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.frame, text="Blood Type").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.blood_type_combo = ttk.Combobox(self.frame, values=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
        self.blood_type_combo.grid(row=1, column=1, padx=10, pady=5)
        self.blood_type_combo.current(0)  # Set default value

        tk.Button(self.frame, text="Predict", command=self.predict).grid(row=2, column=0, columnspan=2, pady=10)
        self.result_label = tk.Label(self.frame, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def predict(self):
        try:
            # Convert the days_ahead input to an integer
            days_ahead = int(self.days_entry.get())

            if days_ahead < 0:
                raise ValueError("Days ahead cannot be negative")

            blood_type = self.blood_type_combo.get()  # Get selected blood type
            prediction = predict_blood_demand(days_ahead, blood_type)

            if prediction is not None:
                result_text = f"Predicted units for {blood_type} in {days_ahead} days:\n{prediction:.2f} units"
                self.result_label.config(text=result_text)
            else:
                self.result_label.config(text="Prediction failed. Please try again.")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of days (non-negative integer).")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print(f"Error in prediction: {e}")


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
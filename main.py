# gui/main.py
import tkinter as tk
from tkinter import ttk, messagebox

from gui.auth import Auth
from gui.donor_entry import DonorEntry
from gui.emergency_dispense import EmergencyDispense
from gui.routine_dispense import RoutineDispense
from gui.view_logs import ViewLogs


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

        if self.tab_control.tabs():  # Only pack if there are tabs
            self.tab_control.pack(expand=1, fill='both')
        else:
            messagebox.showinfo("Access Denied", "You do not have permission to access any tabs.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

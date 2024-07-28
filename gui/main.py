# gui/main.py
import tkinter as tk
from tkinter import ttk

from donor_entry import DonorEntry
from emergency_dispense import EmergencyDispense
from routine_dispense import RoutineDispense
from view_logs import ViewLogs

# Tkinter setup
root = tk.Tk()
root.title("BECS - Blood Donation and Dispensing System")

tab_control = ttk.Notebook(root)

# Donor Entry Tab
donor_entry_tab = DonorEntry(tab_control)
tab_control.add(donor_entry_tab.frame, text='Donor Entry')

# Routine Dispensing Tab
routine_dispensing_tab = RoutineDispense(tab_control)
tab_control.add(routine_dispensing_tab.frame, text='Routine Dispensing')

# Emergency Dispensing Tab
emergency_dispensing_tab = EmergencyDispense(tab_control)
tab_control.add(emergency_dispensing_tab.frame, text='Emergency Dispensing')

# Log Viewing Tab
log_viewing_tab = ViewLogs(tab_control)
tab_control.add(log_viewing_tab.frame, text='Audit Logs')

tab_control.pack(expand=1, fill='both')

root.mainloop()

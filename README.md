# Blood Establishment Computer Software (BECS) Project

## Project Overview

This project is a Blood Establishment Computer Software (BECS) system designed to manage blood donation entries, routine blood dispensing, and emergency blood dispensing. The project is implemented using Python, Tkinter for the graphical user interface (GUI), and SQLAlchemy for database management.

## Features

- **Donor Management**: Enter and store donor information.
- **Routine Blood Dispensing**: Dispense blood units based on requests.
- **Emergency Blood Dispensing**: Handle emergency blood requests efficiently.
- **Audit Trail**: Maintain a security-relevant chronological record of all significant actions.
- **Data Export**: Export all donor, inventory, and log data to a JSON file.

## Requirements

- Python 3.x
- Tkinter
- SQLAlchemy

## Setup Instructions

### Step 1: Install Required Packages

Open a terminal and run the following commands to install the necessary packages:

```bash
pip install tk
pip install sqlalchemy
```

### Step 2: Run The Application

```bash
python gui.py
```

### Usage

#### Donor Management

1. Enter Donor Information: Input the donor’s full name, ID number, blood type, and donation date. Click “Submit” to
   save the information.
2. View Donor Entries: This feature has been removed as donor entries can now be viewed in the Audit Logs tab.

### Routine Blood Dispensing

	1.	Select Blood Type: Choose the requested blood type from the dropdown.
	2.	Enter Number of Units: Input the number of units to dispense.
	3.	Dispense Blood: Click “Dispense Blood” to process the request. The system will log the action and update the inventory.

### Emergency Blood Dispensing

	1.	Dispense Emergency Blood: Click “Dispense Emergency Blood (O-)” to process an emergency request for O- blood. The system will log the action and update the inventory.

### Audit Logs

	1.	View Logs: Navigate to the “Audit Logs” tab to view all logged actions.
	2.	Refresh Logs: Click “Refresh Logs” to update the log display with the latest entries.

### Data Export

	1.	Export Data: Click “Export Data” in the Donor Entry tab to export all donor, inventory, and log data to a JSON file.

### Project Structure

	•	database.py: Defines the database schema and sets up the SQLite database.
	•	gui.py: Implements the GUI and application logic.



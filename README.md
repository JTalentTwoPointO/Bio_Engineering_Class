# Blood Donation and Dispensing System (BECS)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
- [Running the Application](#running-the-application)
- [User Credentials](#user-credentials)

## Overview

The Blood Donation and Dispensing System (BECS) is a HIPAA-compliant application designed to manage blood donations and
dispensing activities. The system supports multiple user roles and ensures the protection of sensitive information.

## Features

- **Admin**: Can define users, perform all actions, and view metadata.
- **User (Blood Bank Worker)**: Can deposit and withdraw blood units.
- **Research Student**: Cannot view personal data of blood donors.
- Role-based access control.
- Secure login with hashed passwords.
- Complies with HIPAA and PART 11 requirements.
- Predictive analytics for future blood demand.

## Project Structure

Project/
├── database.py
├── create_easy_users.py
├── train_model.py
├── gui/
│ ├── init.py
│ ├── main.py
│ ├── auth.py
│ ├── donor_entry.py
│ ├── routine_dispense.py
│ ├── emergency_dispense.py
│ ├── view_logs.py
└── README.md

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- SQLite

### Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd Project
   ```
2. **Install Dependencies:**
   ```bash
    pip install sqlalchemy bcrypt tkinter scikit-learn pandas
3. **Set Up the Database:**
   ```bash
   python database.py
   ```
4. **Create Initial Users:**
   ```bash
   python create_users.py
   ```
5. **Populate Historical Data (if needed):**
    ```bash
   python populate_historical_data.py 
   ```
6. **Train the Model:**
    ```bash
   python train_model.py
   ```

## Running the Application

~~~~
   ```bash
   python gui/main.py
   ```

## User Credentials

- **Admin**
   - Username: `admin`
   - Password: `admin`
- **User (Blood Bank Worker)**
   - Username: `user`
   - Password: `user`
- **Research Student**
   - Username: `student`
   - Password: `student`
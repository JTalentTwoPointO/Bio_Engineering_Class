import os
import random
import sys

from faker import Faker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.database import Session, BloodInventory, Donor

# Initialize Faker to generate realistic random data
fake = Faker()

# Create a session
session = Session()

# Blood types and random unit ranges for inventory
blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
blood_inventory_data = []

# Generate large blood inventory data
for blood_type in blood_types:
    units = random.randint(20, 100)  # Randomize units between 20 and 100
    blood_inventory_data.append({'blood_type': blood_type, 'units': units})

# Insert blood inventory data
for blood_data in blood_inventory_data:
    blood_inventory = BloodInventory(blood_type=blood_data['blood_type'], units=blood_data['units'])
    session.add(blood_inventory)

# Generate large number of donor data
num_donors = 1000  # Let's create 1000 random donors
donor_data = []

for _ in range(num_donors):
    donor_name = fake.name()  # Generate random name
    id_number = fake.unique.ssn()  # Generate a random unique ID
    blood_type = random.choice(blood_types)  # Random blood type
    donation_date = fake.date_between(start_date='-2y', end_date='today')  # Random donation date in the last 2 years
    donor_data.append(
        {'name': donor_name, 'id_number': id_number, 'blood_type': blood_type, 'donation_date': donation_date})

# Insert donor data into the database
for donor in donor_data:
    donor_entry = Donor(name=donor['name'], id_number=donor['id_number'], blood_type=donor['blood_type'],
                        donation_date=donor['donation_date'])
    session.add(donor_entry)

# Commit all changes to the database
session.commit()

print(f"Blood inventory and {num_donors} donor records have been populated.")

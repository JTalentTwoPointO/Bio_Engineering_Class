# train_model.py
import pickle

import pandas as pd
from sklearn.linear_model import LinearRegression

from database import Session, HistoricalData

# Load data from the database
session = Session()
data = session.query(HistoricalData).all()
session.close()

# Convert to DataFrame
df = pd.DataFrame([(d.date, d.blood_type, d.units_used) for d in data], columns=['date', 'blood_type', 'units_used'])

# Prepare the data
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
df = df.groupby(['date', 'blood_type']).sum().unstack().fillna(0)

# Train a linear regression model
X = df.index.factorize()[0].reshape(-1, 1)  # Convert dates to numeric values
y = df.values

model = LinearRegression()
model.fit(X, y)

# Save the model
with open('blood_demand_model.pkl', 'wb') as f:
    pickle.dump(model, f)

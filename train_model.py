import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from database.database import Session, Donor


# Step 1: Load Data from the Donor Table
def load_donor_data():
    session = Session()
    donor_data = session.query(Donor).all()

    # Convert to a pandas DataFrame
    data = [{'date': record.donation_date, 'blood_type': record.blood_type} for record in donor_data]
    df = pd.DataFrame(data)

    df['units_donated'] = np.random.randint(1, 10, size=len(df))  # Adding some diversity
    print("Training data sample:\n", df.head())

    return df


# Step 2: Feature Engineer and Normalize Date
def preprocess_data(df):
    # Convert the donation date to a numerical format (ordinal)
    df['date_numeric'] = pd.to_datetime(df['date']).map(pd.Timestamp.toordinal)

    # Feature engineering: Add day of the week and month as features
    df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek  # Day of the week (0=Monday, 6=Sunday)
    df['month'] = pd.to_datetime(df['date']).dt.month  # Month (1=January, 12=December)

    # Normalize the date_numeric, day_of_week, month, and blood_type_encoded using MinMaxScaler
    scaler = MinMaxScaler()
    features_to_scale = ['date_numeric', 'day_of_week', 'month']
    df[features_to_scale] = scaler.fit_transform(df[features_to_scale])  # Ensure scaler is trained on all 3 features

    # Encode the blood types (A+, B-, etc.)
    label_encoder = LabelEncoder()
    df['blood_type_encoded'] = label_encoder.fit_transform(df['blood_type'])

    # Features: date, day_of_week, month, and blood type
    X = df[['date_numeric', 'day_of_week', 'month', 'blood_type_encoded']]  # Ensure all 4 features are used
    y = df['units_donated']  # Target is the number of units donated

    print("Preprocessed data sample:\n", X.head(), "\nTarget sample:\n", y.head())

    return X, y, label_encoder, scaler


# Step 3: Train the Model
def train_model(X, y):
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize RandomForest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Test the model and print the Mean Squared Error (MSE)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Model trained! Mean Squared Error: {mse}")

    return model


# Step 4: Save the Model to a File
def save_model(model, label_encoder, scaler, filename='blood_demand_model.pkl'):
    # Save the model, label encoder, and scaler
    with open(filename, 'wb') as f:
        pickle.dump({'model': model, 'label_encoder': label_encoder, 'scaler': scaler}, f)
    print(f"Model saved to {filename}")


# Main Program: Train and Save the Model
if __name__ == "__main__":
    # Step 1: Load donor data from the database
    df = load_donor_data()

    # Step 2: Preprocess the data
    X, y, label_encoder, scaler = preprocess_data(df)

    # Step 3: Train the model
    model = train_model(X, y)

    # Step 4: Save the model and label encoder
    save_model(model, label_encoder, scaler)

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Donor(Base):
    __tablename__ = 'donors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_number = Column(String)
    blood_type = Column(String)
    donation_date = Column(Date)

class BloodUnit(Base):
    __tablename__ = 'blood_units'
    id = Column(Integer, primary_key=True)
    donor_id = Column(Integer)
    blood_type = Column(String)
    donation_date = Column(Date)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    blood_type = Column(String)
    units_requested = Column(Integer)
    transaction_date = Column(Date)
    transaction_type = Column(String)
    status = Column(String)

# Create an SQLite database
engine = create_engine('sqlite:///becs.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

from datetime import datetime

import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
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

class BloodInventory(Base):
    __tablename__ = 'blood_inventory'
    id = Column(Integer, primary_key=True)
    blood_type = Column(String)
    units = Column(Integer)

class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(String)
    details = Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)


class HistoricalData(Base):
    __tablename__ = 'historical_data'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    blood_type = Column(String, nullable=False)
    units_used = Column(Integer, nullable=False)

engine = create_engine('sqlite:///becs.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
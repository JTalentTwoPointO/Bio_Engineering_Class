from datetime import datetime

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

engine = create_engine('sqlite:///becs.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
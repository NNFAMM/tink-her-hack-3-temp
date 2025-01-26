from flask import Flask, jsonify
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Set up the database and session
engine = create_engine('sqlite:///buses.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define the ORM models
class Bus(Base):
    __tablename__ = 'buses'
    bus_id = Column(Integer, primary_key=True, autoincrement=True)
    bus_name = Column(String, nullable=False)
    registration_no = Column(String, nullable=False)

class Stop(Base):
    __tablename__ = 'stops'
    stop_id = Column(Integer, primary_key=True, autoincrement=True)
    stop_name = Column(String, nullable=False)

class Route(Base):
    __tablename__ = 'routes'
    route_id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey('buses.bus_id'), nullable=False)
    stop_id = Column(Integer, ForeignKey('stops.stop_id'), nullable=False)
    start_location = Column(String, nullable=False)
    end_location = Column(String, nullable=False)
    arrival_time = Column(String, nullable=False)

    bus = relationship("Bus")
    stop = relationship("Stop")

# Create tables (if they don't exist already)
Base.metadata.create_all(engine)

# Insert sample data using SQLAlchemy ORM
def insert_sample_data():
    # Create instances of Bus, Stop, and Route
    buses = [
        Bus(bus_name='Bus A', registration_no='REG123'),
        Bus(bus_name='Bus B', registration_no='REG124'),
        Bus(bus_name='Bus C', registration_no='REG125'),
        Bus(bus_name='Bus D', registration_no='REG126'),
        Bus(bus_name='Bus E', registration_no='REG127'),
        Bus(bus_name='Bus F', registration_no='REG128'),
        Bus(bus_name='Bus G', registration_no='REG129'),
        Bus(bus_name='Bus H', registration_no='REG130'),
        Bus(bus_name='Bus I', registration_no='REG131'),
        Bus(bus_name='Bus J', registration_no='REG132')
    ]

    stops = [
        Stop(stop_name='Stop A'),
        Stop(stop_name='Stop B'),
        Stop(stop_name='Stop C'),
        Stop(stop_name='Stop D'),
        Stop(stop_name='Stop E'),
        Stop(stop_name='Stop F'),
        Stop(stop_name='Stop G'),
        Stop(stop_name='Stop H'),
        Stop(stop_name='Stop I'),
        Stop(stop_name='Stop J')
    ]

    # Add buses and stops to session
    session.add_all(buses)
    session.add_all(stops)

    # Commit to save changes
    session.commit()

    # Insert sample data for routes
    routes = [
        Route(bus_id=1, stop_id=1, start_location='Stop A', end_location='Stop E', arrival_time='02:00 AM'),
        Route(bus_id=1, stop_id=2, start_location='Stop A', end_location='Stop E', arrival_time='02:05 AM'),
        Route(bus_id=1, stop_id=3, start_location='Stop A', end_location='Stop E', arrival_time='02:10 AM'),
        Route(bus_id=2, stop_id=4, start_location='Stop B', end_location='Stop F', arrival_time='02:15 AM'),
        Route(bus_id=2, stop_id=5, start_location='Stop B', end_location='Stop F', arrival_time='02:20 AM'),
        Route(bus_id=3, stop_id=6, start_location='Stop C', end_location='Stop G', arrival_time='02:25 AM'),
        Route(bus_id=3, stop_id=7, start_location='Stop C', end_location='Stop G', arrival_time='02:30 AM'),
        Route(bus_id=4, stop_id=8, start_location='Stop D', end_location='Stop H', arrival_time='02:35 AM'),
        Route(bus_id=4, stop_id=9, start_location='Stop D', end_location='Stop H', arrival_time='02:40 AM'),
        Route(bus_id=5, stop_id=10, start_location='Stop E', end_location='Stop I', arrival_time='02:45 AM')
    ]

    # Add routes to session
    session.add_all(routes)
    session.commit()

    print("Sample data inserted successfully.")

# Insert sample data
insert_sample_data()

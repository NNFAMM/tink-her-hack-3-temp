from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_cors import CORS
app = Flask(__name__)

CORS(app)


# Setup the database and session
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

@app.route('/api/stops', methods=['GET'])
def get_stops():
    # Query the database to fetch stops
    stops = session.query(Stop).all()
    # Convert the result to a list of dictionaries
    stops_data = [{'name': stop.stop_name} for stop in stops]
    return jsonify(stops_data)


# Route to fetch routes from the database
@app.route('/api/routes', methods=['GET'])
def get_routes():
    # Query the database to fetch routes
    routes = session.query(Route).all()
    # Convert the result to a list of dictionaries
    routes_data = [{'startLocation': route.start_location, 'endLocation': route.end_location} for route in routes]
    return jsonify(routes_data)

# Endpoint for searching routes or stops
@app.route('/search', methods=['GET'])
def search():
    search_type = request.args.get('type')
    search_value = request.args.get('value')
    
    if search_type == 'stop':
        stops = session.query(Stop, Route).join(Route).filter(Stop.stop_name == search_value)
        result = [{"Bus_Name": stop.bus.bus_name, "Registration_No": stop.bus.registration_no, "Arrival_Time": route.arrival_time} for stop, route in stops]
    elif search_type == 'route':
        start_location = search_value('startLocation')
        end_location = search_value('endLocation')
        routes = session.query(Route).filter(Route.start_location == start_location, Route.end_location == end_location).all()
        result = [{"Bus_Number": route.bus.bus_name, "Arrival_Time": route.arrival_time, "Route_Name": f"{route.start_location} to {route.end_location}"} for route in routes]
    else:
        result = []

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

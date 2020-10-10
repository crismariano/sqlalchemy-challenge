import sqlalchemy
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Routes
#################################################

@app.route("/")
def Home():
    """List all routes that are available."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    ) 


@app.route("/api/v1.0/precipitation")
def precipitation():
 
    session = Session(engine)

    """Return Dates and Precipitation data in dictionary format"""
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()

    prcp_date = dict(precipitation_data)
    
    return jsonify(prcp_date)
    
@app.route("/api/v1.0/stations")
def stations():
 
    session = Session(engine)

    """List of Stations"""
    station_data = session.query(Measurement.station).group_by(Measurement.station)
    station_name = list(station_data)
    
    return jsonify(station_name) 

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
 
    """Temperature Observation Data"""
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').\
        filter(Measurement.station == "USC00519281").all()    
    
    # Create a list of dates and tobs
    tobs_list = list(tobs_data)

    return jsonify(tobs_list) 

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):

    session = Session(engine)

    """List of minimum temperature, the average temperature, and the max temperature for a give start date"""

    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date ).all()

    date_start = []

    for temp in temps:
        temp_data = {}
        temp_data["Start Date"] = start_date
        temp_data["Minimum Temperature"] = temp[0]
        temp_data["Average Temperature"] = temp[1]
        temp_data["Maximum Temperature"] = temp[2]
        date_start.append(temp_data)

    return jsonify(date_start)


@app.route("/api/v1.0/<start_date>/<end_date>")
def vacation_dates(start_date, end_date):

    session = Session(engine)

    """List of minimum temperature, the average temperature, and the max temperature for a give start date"""

    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    vaca_dates = []

    for temp in temps:
        temp_data = {}
        temp_data["Start Date"] = start_date
        temp_data["End Date"] = end_date
        temp_data["Minimum Temperature"] = temp[0]
        temp_data["Average Temperature"] = temp[1]
        temp_data["Maximum Temperature"] = temp[2]
        vaca_dates.append(temp_data)

    return jsonify(vaca_dates)


if __name__ == '__main__':
    app.run(debug=True)

    







import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


app = Flask(__name__)


@app.route("/")
def home():
    """List all available routes"""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/&lt;start&gt;'>/api/v1.0/&lt;start&gt;</a><br/>"
        f"<a href='/api/v1.0/&lt;start&gt;/&lt;end&gt;'>/api/v1.0/&lt;start&gt;/&lt;end&gt;</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').all()
    prcp_dict = {date: prcp for date, prcp in prcp_data}
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    station_data = session.query(Station.station, Station.name).all()
    station_list = list(station_data)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations for the previous year"""
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station == 'USC00519281').all()
    tobs_list = list(tobs_data)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return TMIN, TAVG, and TMAX for all dates greater than or equal to start date"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    temp_list = list(np.ravel(results))
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return TMIN, TAVG, and TMAX for dates between start and end date inclusive"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).\
              filter(Measurement.date <= end).all()
    temp_list = list(np.ravel(results))
    return jsonify(temp_list)


if __name__ == '__main__':
    app.run(debug=True)

from ast import And
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import json

engine = create_engine('sqlite:///hawaii.sqlite?check_same_thread=False')
base = automap_base()
base.prepare(engine, reflect=True)
Measurement = base.classes.measurement
Station = base.classes.station
session = Session(engine)
# Inspector = inspect(engine)
# print(Inspector.get_table_names())
# for c in Inspector.get_columns(('Measurement','Station')):
#     print(c['name'], c['type'])


app = Flask('blah')
@app.route('/')
def welcome():
    return ('''Welcome to the Climate Analysis API!<br \>
    Available Routes:<br \>
    /api/v1.0/precipitation<br \>
    /api/v1.0/stations<br \>
    /api/v1.0/tobs<br \>
    /api/v1.0/temp/start/end''')
@app.route('/api/v1.0/precipitation')
def precipitation():
    prev_year = dt.datetime(2017, 8, 23)-dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in results}
    return jsonify(precip)
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(Stations=stations)
@app.route('/api/v1.0/tobs')
def tobs():
    prev_year = dt.datetime(2017, 8, 23)-dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= prev_year).all()
    r_results = list(np.ravel(results))
    temp = jsonify(Temperature=r_results)
    return (temp)
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(Temperature=temps)
    results = session.query(*sel).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(Temperature=temps)

# import app
# print("example __name__ = %s", __name__)

# if __name__ == "__main__":
#     print("example is being run directly.")
# else:
#     print("example is being imported")


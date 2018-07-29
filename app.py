from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import *

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/database.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurements
Stations = Base.classes.stations

session = Session(engine)

app = Flask(__name__)

#http://localhost:5000/api/v1.0/precipitation/
@app.route("/api/v1.0/precipitation/")
def precip_for_year():
    temps_for_top_stations = (
        session.query(Measurements.date, Measurements.tobs)
            .filter(and_(Measurements.date >= '2015-06-12', Measurements.date <= '2016-06-12'))
            .filter(Measurements.station == 'USC00519281')
    ).all()

    temp_dict = {}
    for temp in temps_for_top_stations:
        temp_dict[str(temp.date)] = temp.tobs

    return jsonify(temp_dict)

# http://localhost:5000/api/v1.0/stations
@app.route("/api/v1.0/stations")
def list_of_stations():
    stations = session.query(Stations.station).distinct().all()

    stations_list = []
    for station in stations:
        stations_list.append(station.station)

    return jsonify(stations_list)

# http://localhost:5000/api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    tobs = (
        session.query(Measurements.tobs)
        .filter(and_(Measurements.date >= '2015-06-12', Measurements.date <= '2016-06-12'))
    ).all()

    tobs_list = []
    for tob in tobs:
        tobs_list.append(tob.tobs)

    return jsonify(tobs_list)

#http://localhost:5000/api/v1.0/<start_date>
@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    temps_above = (session
            .query(Measurements.tobs,
                  func.min(Measurements.tobs).label('min_temp'),
                  func.max(Measurements.tobs).label('max_temp'),
                  func.avg(Measurements.tobs).label('avg_temp'))
            .filter(Measurements.date >= start_date)
            .filter(Measurements.station == 'USC00519281'))
    min = temps_above.one().min_temp
    max = temps_above.one().max_temp
    avg = temps_above.one().avg_temp
    print("Min. Temp: " + str(min))
    print("Max. Temp: " + str(max))
    print("Avg. Temp: " + str(avg))
    return jsonify([min, max, avg])

#http://localhost:5000/api/v1.0/<start_date>/<end_date>
@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    temps_inclusive = (session
            .query(Measurements.tobs,
                  func.min(Measurements.tobs).label('min_temp'),
                  func.max(Measurements.tobs).label('max_temp'),
                  func.avg(Measurements.tobs).label('avg_temp'))
            .filter(and_(Measurements.date >= start_date, Measurements.date <= end_date))
            .filter(Measurements.station == 'USC00519281'))
    min = temps.one().min_temp
    max = temps.one().max_temp
    avg = temps.one().avg_temp
    print("Min. Temp: " + str(min))
    print("Max. Temp: " + str(max))
    print("Avg. Temp: " + str(avg))
    return jsonify([min, max, avg])

if __name__ == '__main__':
    app.run(debug=True)

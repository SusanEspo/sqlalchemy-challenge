# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()


# # reflect the tables
Base.prepare(autoload_with=engine)

#Base.classes.keys()

# # # Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# # # Create our session (link) from Python to the DB
session = Session(engine)

# #################################################
# # Flask Setup
# #################################################
app = Flask(__name__)



# #################################################
# # Flask Routes
# #################################################

@app.route("/")
def home ():
    return (
        "Welcome to the analysis of precipitation!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start<br/>"
        "/api/v1.0/startandend"
    )
    
    
##----------------------------------------------------------
@app.route("/api/v1.0/precipitation")
def prcp():
     #print("Server received request for 'precipitation' page...")
     #return "Welcome to my 'precipitation' page!"

# # # ##----------------------------------------------------------
# # # #Convert the query results from your precipitation analysis 
# # #(i.e. retrieve only the last 12 months of data) 
# # # #to a dictionary using date as the key and prcp as the value.


    precip_data_list = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > (dt.date(2017,8,23)- dt.timedelta(days = 365)) ).all()
     #precip_data_list
#df_pc = pd.DataFrame(precip_data_list )
# #df_pc
    date_list=[]
    precip_data_dict = {}
    for p_data in precip_data_list:
        dateKey = p_data[0]
        prcp = p_data[1]
        if dateKey not in date_list:
            date_list.append(dateKey)
            precip_data_dict.update({dateKey: prcp })

# #print (precip_data_dict)
# #precip_data_dict
 
#Return the JSON representation of your dictionary.
    return jsonify(precip_data_dict)

    session.close()

# ################################


@app.route("/api/v1.0/stations")
def stations():
    
    
#Create our session (link) from Python to the DB
        session = Session(engine)

#     """Return a list of all station names"""
#     # Query all stations
        station_cnt = session.query(Station.station).all()
        print(station_cnt)
        session.close()

# Convert list of tuples into normal list
        all_stations = list(np.ravel(station_cnt))

        return jsonify(stations=all_stations)
    
       
#     print("Server received request for 'stations' page...")
#     return "Welcome to my 'stations' page!" 



# @app.route("/api/v1.0/tobs")
# def tobs():
#     #Create our session (link) from Python to the DB
#     session = Session(engine)
            
#     # active_station =session.query(Measurement.station, func.count(Measurement.station)).\
#     # group_by(Measurement.station).\
#     # order_by(func.count(Measurement.station).desc()).all()


# #active_station

#     #temp_data = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date > (dt.date(2017,8,23)- dt.timedelta(days = 365)), Measurement.station == "USC00519281").all()
#     temp_data = session.query(Measurement.tobs).filter(Measurement.date > (dt.date(2017,8,23)- dt.timedelta(days = 365)), Measurement.station == "USC00519281").all()
#     df_temp_data =  pd.DataFrame(temp_data)

#     #df_temp_data 
#     ##temp_data
    
#     session.close()
    
#     return jsonify(df_temp_data)
# #    print("Server received request for 'tobs' page...")
# #    return "Welcome to my 'tobs' page!" 



# @app.route("/api/v1.0/start")
# def start():
#     print("Server received request for 'start' page...")
#     return "Welcome to my 'start' page!" 




# @app.route("/api/v1.0/startandend")
# def start():
#     print("Server received request for 'start' page...")
#     return "Welcome to my 'start' page!" 

if __name__ == "__main__":
     app.run(debug=True)

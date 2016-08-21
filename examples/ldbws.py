#!/usr/bin/env python3
#
# This file contains an example of how to make a very basic use of this library to query all the
# departures at a station using the LDBWS API. For more detailed information on how to use this
# library, and all the web services, API endpoints and objects and properties that you can use
# with this library, please see the API docs at http://nrewebservices.readthedocs.org
#
# ***** This example will only work if you fill in your LDBWS API key below. *****
#

from nrewebservices.ldbws import Session

# Set up the address for the LDBWS and your API key.
API_URL = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16"
API_KEY = "PASTE YOUR LDBWS API KEY HERE"

# Instantiate the web service session.
session = Session(API_URL, API_KEY)

# Get a departure board containing the next ten departures from Reading.
board = session.get_station_board("RDG", rows=10, include_departures=True, include_arrivals=False)

print("The next 10 departures from Reading are:")

# Loop over all the train services in that board.
for service in board.train_services:
    
    # Build a list of destinations for each train service.
    destinations = [destination.location_name for destination in service.destinations]

    # Print some basic information about that train service.
    print("{} to {}: due {}.".format(
        service.std,
        ",".join(destinations),
        service.etd
    ))



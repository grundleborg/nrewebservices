import os
import sys

testsPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testsPath + '/../')

from suds.client import Client

import datetime
import pytest
import pytz

from nrewebservices.ldbws import Session, StationBoard

from helpers import mock_ldbws_response_from_file, ldbws_client_helper

@pytest.fixture(scope="module")
def board():
    ldbws_client = ldbws_client_helper()
    response = mock_ldbws_response_from_file(
            ldbws_client, 
            "LDBServiceSoap", 
            "GetDepartureBoard",
            "basic-station-board-departures.xml",
    )
    return StationBoard(response)

class TestStationBoardDepartures(object):

    def test_station_board_basics(self, board):
        # Basic StationBoard properties.
        assert board.generated_at.astimezone(pytz.utc) == \
                datetime.datetime(2016, 8, 6, 21, 7, 1, 602815, tzinfo=pytz.utc)
        assert board.location_name == 'East Croydon'
        assert board.crs == 'ECR'
        assert board.filter_location_name is None
        assert board.filter_crs is None
        assert board.filter_type is None
        assert board.platform_available is True

        # This one does not appear to be reported as per the online documentation.
        assert board.services_available is None
        
        # NRCC messages list.
        assert board.nrcc_messages == ['<P>Amended weekday Southern and Gatwick Express services. More information in <A href="http://nationalrail.co.uk/service_disruptions/143147.aspx">Latest Travel News</A>.</P>']
        
        # Services Lists
        assert len(board.train_services) == 10
        assert len(board.bus_services) == 0
        assert len(board.ferry_services) == 0

    def test_station_board_train_service_basics(self, board):
        # Basic service properties.
        service = board.train_services[1]
        assert len(service.origins) == 1
        assert len(service.destinations) == 1
        assert len(service.current_origins) == 0
        assert len(service.current_destinations) == 0
        #assert service.sta == datetime.time(0, 1, 2)
        # TODO: All the rest...

    def test_station_board_train_service_origin_basics(self, board):
        # Basic service location properties.
        origin = board.train_services[1].origins[0]
        assert origin.location_name == "Horsham"
        assert origin.crs == "HRH"
        assert origin.via is None
        assert origin.future_change_to is None
        assert origin.association_is_cancelled is None

    # TODO:
    #   - Test Destination.
    #   - Test one with a Bus Service.
    #   - Test one with a Ferry Service.
    #   - Test one with a via location filled in.
    #   - Test one with a current origin.
    #   - Test one with a current destination.
    #   - Test one with the platforms hidden.
    #   - Test one with the services hidden.



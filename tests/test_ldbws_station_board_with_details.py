import os
import sys

testsPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testsPath + '/../')

from suds.client import Client

import datetime
import pytest
import pytz

from nrewebservices.ldbws import Session, StationBoardWithDetails

from helpers import mock_ldbws_response_from_file, ldbws_client_helper

@pytest.fixture(scope="module")
def board():
    ldbws_client = ldbws_client_helper()
    response = mock_ldbws_response_from_file(
            ldbws_client, 
            "LDBServiceSoap", 
            "GetDepBoardWithDetails",
            "basic-station-board-with-details-departures.xml",
    )
    return StationBoardWithDetails(response)

class TestStationBoardWithDetailsDepartures(object):

    def test_station_board_with_details_basics(self, board):
         # Basic StationBoard properties.
        assert board.generated_at.astimezone(pytz.utc) == \
                datetime.datetime(2016, 8, 6, 21, 5, 47, 752888, tzinfo=pytz.utc)
        assert board.location_name == 'East Croydon'
        assert board.crs == 'ECR'
        assert board.filter_location_name is None
        assert board.filter_crs is None
        assert board.filter_type is None
        assert board.platforms_available is True
        assert board.services_available is True
        
        # NRCC messages list.
        assert board.nrcc_messages == ['<P>Amended weekday Southern and Gatwick Express services. More information in <A href="http://nationalrail.co.uk/service_disruptions/143147.aspx">Latest Travel News</A>.</P>']
        
        # Services Lists
        assert len(board.train_services) == 10
        assert len(board.bus_services) == 0
        assert len(board.ferry_services) == 0

    def test_station_board_with_details_train_service_basics(self, board):
        # Basic service properties.
        service = board.train_services[1]
        assert len(service.origins) == 1
        assert len(service.destinations) == 1
        assert len(service.current_origins) == 0
        assert len(service.current_destinations) == 0
        assert service.sta is None
        assert service.eta is None
        assert service.std == "22:03"
        assert service.etd == "22:15"
        assert service.platform == "1"
        assert service.operator == "Southern"
        assert service.operator_code == "SN"
        assert service.circular_route is False
        assert service.cancelled is False
        assert service.filter_location_cancelled is False
        assert service.service_type == "train"
        assert service.length is None
        assert service.detach_front is False
        assert service.reverse_formation is False
        assert service.cancel_reason is None
        assert service.delay_reason is None
        assert service.service_id == "l4/FfBv9+LeshRsit6lwzw=="
        assert service.adhoc_alerts == None
        assert service.rsid == "SN083300"
        assert service.origin == "Horsham"
        assert service.destination == "London Victoria"

    def test_station_board_with_details_service_calling_points(self, board):
        service = board.train_services[1]

        # Check the quantity of each type of calling point list.
        assert len(service.previous_calling_points) == 0
        assert len(service.subsequent_calling_points) == 1

        # Check the subsequent calling points list properties.
        scp = service.subsequent_calling_points[0]
        assert len(scp) == 2
        assert scp.service_type == None
        assert scp.change_required == False
        assert scp.association_is_cancelled == False

        # Check the actual calling point properties.
        cp = scp[0]
        cp.location_name
        assert cp.location_name == "Clapham Junction"
        assert cp.crs == "CLJ"
        assert cp.st == "22:12"
        assert cp.et == "22:24"
        assert cp.at is None
        assert cp.cancelled is False
        assert cp.length is None
        assert cp.detach_front is False
        assert cp.adhoc_alerts is None



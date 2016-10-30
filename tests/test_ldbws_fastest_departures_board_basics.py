import os
import sys

testsPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testsPath + '/../')

from suds.client import Client

import datetime
import pytest
import pytz

from nrewebservices.ldbws import NextDeparturesBoard, Session

from helpers import mock_ldbws_response_from_file, ldbws_client_helper

@pytest.fixture(scope="module")
def board():
    ldbws_client = ldbws_client_helper()
    response = mock_ldbws_response_from_file(
            ldbws_client, 
            "LDBServiceSoap", 
            "GetFastestDepartures",
            "basic-fastest-departures-board.xml",
    )
    return NextDeparturesBoard(response)

class TestFastestDeparturesBoard(object):

    def test_fastest_departures_board_basics(self, board):
        # Basic NextDeparturesBoard properties.
        assert board.generated_at.astimezone(pytz.utc) == \
                datetime.datetime(2016, 8, 6, 21, 11, 44, 678600, tzinfo=pytz.utc)
        assert board.location_name == 'East Croydon'
        assert board.crs == 'ECR'
        assert board.filter_location_name is None
        assert board.filter_crs is None
        assert board.filter_type is None
        assert board.platforms_available is True
        assert board.services_available is True
        
        # NRCC messages list.
        assert board.nrcc_messages == ['<P>Amended weekday Southern and Gatwick Express services. More information in <A href="http://nationalrail.co.uk/service_disruptions/143147.aspx">Latest Travel News</A>.</P>']

        # Next Departures items.
        assert len(board.next_departures) == 3

    def test_fastest_departures_board_next_departures_basics(self, board):
        dep = board.next_departures[1]
        assert dep.crs == "GTW"

    def test_fastest_departures_board_service_basics(self, board):
        service = board.next_departures[1].service
        assert len(service.origins) == 1
        assert len(service.destinations) == 1
        assert len(service.current_origins) == 0
        assert len(service.current_destinations) == 0
        assert service.sta == "22:05"
        assert service.eta == "22:09"
        assert service.std == "22:06"
        assert service.etd == "22:11"
        assert service.platform == "2"
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
        assert service.service_id == "1hHszdehfteYvCy6NbiPKw=="
        assert service.adhoc_alerts == None
        assert service.rsid == "SN078700"
        assert service.origin == "London Victoria"
        assert service.destination == "Brighton"


import os
import sys

testsPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testsPath + '/../')

from suds.client import Client

import datetime
import pytest
import pytz

from nrewebservices.ldbws import ServiceDetails, Session, StationBoard

from helpers import mock_ldbws_response_from_file, ldbws_client_helper

@pytest.fixture(scope="module")
def board():
    ldbws_client = ldbws_client_helper()
    response = mock_ldbws_response_from_file(
            ldbws_client, 
            "LDBServiceSoap", 
            "GetDepartureBoard",
            "departure-board-with-partial-formation-and-loading.xml",
    )
    return StationBoard(response)

class TestStationBoardDepartures(object):

    def test_station_board_basics(self, board):
        # Basic StationBoard properties.
        assert board.generated_at.astimezone(pytz.utc) == \
                datetime.datetime(2018, 11, 5, 17, 35, 13, 157859, tzinfo=pytz.utc)
        assert board.crs == 'GTW'
        assert board.filter_location_name is None
        assert board.filter_crs is None
        assert board.filter_type is None
        assert board.platforms_available is True
        assert board.services_available is True
        
        # Get the serice with some formation-loading data.
        service = board.train_services[7]

        assert service.origin == 'Brighton'
        assert service.destination == 'London Victoria'
        assert service.formation is not None

        formation = service.formation
        
        assert formation.average_loading is None
        assert len(formation.coaches) == 8

        coach = formation.coaches[0]
        
        assert coach.number == '0'
        assert coach.coach_class == 'Standard'
        assert coach.loading == 93
        assert coach.toilet_type == 'None'
        assert coach.toilet_status == 'Unknown'

        coach = formation.coaches[1]
        assert coach.number == '1'
        assert coach.coach_class == 'Standard'
        assert coach.loading == 100
        assert coach.toilet_type == 'Accessible'
        assert coach.toilet_status == 'Unknown'

@pytest.fixture(scope="module")
def service():
    ldbws_client = ldbws_client_helper()
    response = mock_ldbws_response_from_file(
            ldbws_client,
            "LDBServiceSoap",
            "GetServiceDetails",
            "service-details-with-partial-formation-and-loading.xml",
    )
    return ServiceDetails(response)

class TestServiceDetails(object):

    def test_service_details_basics(self, service):
        assert service.generated_at.astimezone(pytz.utc) == \
                datetime.datetime(2018, 11, 5, 18, 52, 2, 946586, tzinfo=pytz.utc)
        assert service.service_type == 'train'
        assert service.location_name == 'Gatwick Airport'
        assert service.crs == 'GTW'
        assert service.operator == 'Gatwick Express'
        assert service.operator_code == 'GX'

        assert service.formation is not None

        formation = service.formation

        assert formation.average_loading is None
        assert len(formation.coaches) == 12

        coach = formation.coaches[0]

        assert coach.number == '0'
        assert coach.coach_class == ''
        assert coach.loading == 83
        assert coach.toilet_type == 'Unknown'
        assert coach.toilet_status == 'Unknown'

        coach = formation.coaches[1]
        assert coach.number == '1'
        assert coach.coach_class == ''
        assert coach.loading == 42
        assert coach.toilet_type == 'Unknown'
        assert coach.toilet_status == 'Unknown'



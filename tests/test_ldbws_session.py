import os
import sys

testsPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testsPath + '/../')

import os
import pytest

from nrewebservices.ldbws import Session

API_URL = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16"

@pytest.fixture(scope="module")
def session():
    return Session(API_URL)

@pytest.mark.skipif(os.environ.get("NRE_LDBWS_API_KEY") is None,
                    reason="NRE_LDBWS_API_KEY must be set to test ldbws.Session class.")
class TestSession(object):

    def test_get_station_board_arrivals(self, session):
        r = session.get_station_board("PAD", rows=10, include_departures=False, include_arrivals=True)

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None

    def test_get_station_board_departures(self, session):
        r = session.get_station_board("PAD", rows=10, include_departures=True, include_arrivals=False)

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None

    def test_get_station_board_arrivals_departures(self, session):
        r = session.get_station_board("PAD", rows=10, include_departures=True, include_arrivals=True)

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None

    def test_get_station_board_neither(self, session):
        with pytest.raises(ValueError):
            r = session.get_station_board("PAD", rows=10, include_departures=False, include_arrivals=False)

    def test_get_station_board_arrivals_filtered_from(self, session):
        r = session.get_station_board("PAD", rows=10, include_departures=False,
                include_arrivals=True, from_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        assert r.filter_type == "from"

    def test_get_station_board_departures_filtered_from(self, session):
        r = session.get_station_board("PAD", rows=10, include_departures=True,
                include_arrivals=False, from_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        assert r.filter_type == "from"

    def test_get_station_board_arrivals_departures_filtered_from(self, session):
        r = session.get_station_board("PAD", rows=10, include_departures=True,
                include_arrivals=True, from_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        assert r.filter_type == "from"

    @pytest.mark.xfail
    def test_get_station_board_arrivals_filtered_to(self, session):
        r = session.get_station_board("PAD", rows=10, include_departures=False,
                include_arrivals=True, to_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        # TODO: Investigate why filter_type is None, not "to".
        assert r.filter_type == "to"

    @pytest.mark.xfail
    def test_get_station_board_departures_filtered_to(self, session):
        r = session.get_station_board("PAD", rows=10, include_departures=True,
                include_arrivals=False, to_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        # TODO: Investigate why filter_type is None, not "to".
        assert r.filter_type == "to"

    @pytest.mark.xfail
    def test_get_station_board_arrivals_departures_filtered_to(self, session):
        r = session.get_station_board("PAD", rows=10, include_departures=True,
                include_arrivals=True, to_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        # TODO: Investigate why filter_type is None, not "to".
        assert r.filter_type == "to"

    @pytest.mark.xfail
    def test_get_station_board_arrivals_filtered_both_filters(self, session):
        r = session.get_station_board("PAD", rows=10, include_departures=False,
                include_arrivals=True, from_filter_crs="RDG", to_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        # TODO: Investigate why filter_type is None, not "to".
        assert r.filter_type == "to"

    ### NEXT ###

    def test_get_station_board_with_details_arrivals(self, session):
        r = session.get_station_board_with_details("PAD", rows=10, include_departures=False, include_arrivals=True)

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None

    def test_get_station_board_with_details_departures(self, session):
        r = session.get_station_board_with_details("PAD", rows=10, include_departures=True, include_arrivals=False)

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None

    def test_get_station_board_with_details_arrivals_departures(self, session):
        r = session.get_station_board_with_details("PAD", rows=10, include_departures=True, include_arrivals=True)

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None

    def test_get_station_board_with_details_neither(self, session):
        with pytest.raises(ValueError):
            r = session.get_station_board_with_details("PAD", rows=10, include_departures=False, include_arrivals=False)

    def test_get_station_board_arrivals_with_details_filtered_from(self, session):
        r = session.get_station_board_with_details("PAD", rows=10, include_departures=False,
                include_arrivals=True, from_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        assert r.filter_type == "from"

    def test_get_station_board_departures_with_details_filtered_from(self, session):
        r = session.get_station_board_with_details("PAD", rows=10, include_departures=True,
                include_arrivals=False, from_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        assert r.filter_type == "from"

    def test_get_station_board_arrivals_departures_with_details_filtered_from(self, session):
        r = session.get_station_board_with_details("PAD", rows=10, include_departures=True,
                include_arrivals=True, from_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        assert r.filter_type == "from"

    @pytest.mark.xfail
    def test_get_station_board_arrivals_with_details_filtered_to(self, session):
        r = session.get_station_board_with_details("PAD", rows=10, include_departures=False,
                include_arrivals=True, to_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        # TODO: Investigate why filter_type is None, not "to".
        assert r.filter_type == "to"

    @pytest.mark.xfail
    def test_get_station_board_departures_with_details_filtered_to(self, session):
        r = session.get_station_board_with_details("PAD", rows=10, include_departures=True,
                include_arrivals=False, to_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        # TODO: Investigate why filter_type is None, not "to".
        assert r.filter_type == "to"

    @pytest.mark.xfail
    def test_get_station_board_arrivals_departures_with_details_filtered_to(self, session):
        r = session.get_station_board_with_details("PAD", rows=10, include_departures=True,
                include_arrivals=True, to_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        # TODO: Investigate why filter_type is None, not "to".
        assert r.filter_type == "to"

    @pytest.mark.xfail
    def test_get_station_board_arrivals_with_details_filtered_both_filters(self, session):
        r = session.get_station_board_with_details("PAD", rows=10, include_departures=False,
                include_arrivals=True, from_filter_crs="RDG", to_filter_crs="RDG")

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name == "Reading"
        assert r.filter_crs == "RDG"
        # TODO: Investigate why filter_type is None, not "to".
        assert r.filter_type == "to"



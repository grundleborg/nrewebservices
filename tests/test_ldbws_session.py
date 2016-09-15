import os
import sys

testsPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testsPath + '/../')

from suds import WebFault

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

    def test_get_next_departures_basic(self, session):
        r = session.get_next_departures("PAD", ["RDG", "TWY"])

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None
        assert len(r.next_departures) == 2

        assert r.next_departures[0].crs == "RDG"
        assert r.next_departures[1].crs == "TWY"

    def test_get_next_departures_not_a_list(self, session):
        with pytest.raises(ValueError):
            r = session.get_next_departures("PAD", "RDG")

    def test_get_next_departures_too_few(self, session):
        with pytest.raises(ValueError):
            r = session.get_next_departures("PAD", [])

    def test_get_next_departures_too_many(self, session):
        with pytest.raises(ValueError):
            r = session.get_next_departures("PAD", ["RDG", "TWY", "PLY", "PNZ", "WAT", "WIN", "BRI", "STP", "LEI", "MIM", "OXF", "CBG", "ABY", "STS", "LSK", "CSK", "GSL", "CLJ", "WIJ", "WAT", "MKC", "BIR", "BMS", "BSH", "MYB", "OPY"])

    def test_get_next_departures_repeated(self, session):
        r = session.get_next_departures("PAD", ["RDG", "TWY", "RDG"])

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None
        assert len(r.next_departures) == 3

        assert r.next_departures[0].crs == "RDG"
        assert r.next_departures[1].crs == "TWY"
        assert r.next_departures[2].crs == "RDG"

    def test_get_next_departures_with_details_basic(self, session):
        r = session.get_next_departures_with_details("PAD", ["RDG", "TWY"])

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None
        assert len(r.next_departures) == 2

        assert r.next_departures[0].crs == "RDG"
        assert r.next_departures[1].crs == "TWY"

    def test_get_next_departures_with_details_not_a_list(self, session):
        with pytest.raises(ValueError):
            r = session.get_next_departures_with_details("PAD", "RDG")

    def test_get_next_departures_with_details_too_few(self, session):
        with pytest.raises(ValueError):
            r = session.get_next_departures_with_details("PAD", [])

    def test_get_next_departures_with_details_too_many(self, session):
        with pytest.raises(ValueError):
            r = session.get_next_departures_with_details("PAD", ["RDG", "TWY", "PLY", "PNZ", "WAT", "WIN", "BRI", "STP", "LEI", "MIM", "OXF", "CBG", "ABY", "STS", "LSK", "CSK", "GSL", "CLJ", "WIJ", "WAT", "MKC", "BIR", "BMS", "BSH", "MYB", "OPY"])

    def test_get_next_departures_with_details_repeated(self, session):
        r = session.get_next_departures_with_details("PAD", ["RDG", "TWY", "RDG"])

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None
        assert len(r.next_departures) == 3

        assert r.next_departures[0].crs == "RDG"
        assert r.next_departures[1].crs == "TWY"
        assert r.next_departures[2].crs == "RDG"

    def test_get_fastest_departures_basic(self, session):
        r = session.get_fastest_departures("PAD", ["RDG", "TWY"])

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None
        assert len(r.next_departures) == 2

        assert r.next_departures[0].crs == "RDG"
        assert r.next_departures[1].crs == "TWY"

    def test_get_fastest_departures_not_a_list(self, session):
        with pytest.raises(ValueError):
            r = session.get_fastest_departures("PAD", "RDG")

    def test_get_fastest_departures_too_few(self, session):
        with pytest.raises(ValueError):
            r = session.get_fastest_departures("PAD", [])

    def test_get_fastest_departures_too_many(self, session):
        with pytest.raises(ValueError):
            r = session.get_fastest_departures("PAD", ["RDG", "TWY", "PLY", "PNZ", "WAT", "WIN", "BRI", "STP", "LEI", "MIM", "OXF", "CBG", "ABY", "STS", "LSK", "CSK", "GSL", "CLJ", "WIJ", "WAT", "MKC", "BIR", "BMS", "BSH", "MYB", "OPY"])

    def test_get_next_fastestrtures_repeated(self, session):
        r = session.get_fastest_departures("PAD", ["RDG", "TWY", "RDG"])

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None
        assert len(r.next_departures) == 3

        assert r.next_departures[0].crs == "RDG"
        assert r.next_departures[1].crs == "TWY"
        assert r.next_departures[2].crs == "RDG"

    def test_get_fastest_departures_with_details_basic(self, session):
        r = session.get_fastest_departures_with_details("PAD", ["RDG", "TWY"])

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None
        assert len(r.next_departures) == 2

        assert r.next_departures[0].crs == "RDG"
        assert r.next_departures[1].crs == "TWY"

    def test_get_fastest_departures_with_details_not_a_list(self, session):
        with pytest.raises(ValueError):
            r = session.get_fastest_departures_with_details("PAD", "RDG")

    def test_get_fastest_departures_with_details_too_few(self, session):
        with pytest.raises(ValueError):
            r = session.get_fastest_departures_with_details("PAD", [])

    def test_get_fastest_departures_with_details_too_many(self, session):
        with pytest.raises(ValueError):
            r = session.get_fastest_departures_with_details("PAD", ["RDG", "TWY", "PLY", "PNZ", "WAT", "WIN", "BRI", "STP", "LEI", "MIM", "OXF", "CBG", "ABY", "STS", "LSK", "CSK", "GSL", "CLJ", "WIJ", "WAT", "MKC", "BIR", "BMS", "BSH", "MYB", "OPY"])

    def test_get_fastest_departures_with_details_repeated(self, session):
        r = session.get_fastest_departures_with_details("PAD", ["RDG", "TWY", "RDG"])

        assert r.location_name == "London Paddington"
        assert r.crs == "PAD"
        assert r.filter_location_name is None
        assert r.filter_crs is None
        assert r.filter_type is None
        assert len(r.next_departures) == 3

        assert r.next_departures[0].crs == "RDG"
        assert r.next_departures[1].crs == "TWY"
        assert r.next_departures[2].crs == "RDG"

    def test_get_service(self, session):
        r = session.get_station_board("PAD", include_departures=True, include_arrivals=False)
        assert len(r.train_services) > 0

        s = session.get_service_details(r.train_services[0].service_id)

        assert s.crs == "PAD"

    def test_get_service_invalid_id(self, session):
        # TODO: Wrap up SUDS errors in something more helpful in the API.
        with pytest.raises(WebFault):
            s = session.get_service_details("lalalalala")



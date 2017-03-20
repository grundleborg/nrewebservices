import os
import sys

testsPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, testsPath + '/../')

from suds.client import Client

import datetime
import pytest
import pytz

from nrewebservices.ldbws import ServiceDetails, Session

from helpers import mock_ldbws_response_from_file, ldbws_client_helper

@pytest.fixture(scope="module")
def service():
    ldbws_client = ldbws_client_helper()
    response = mock_ldbws_response_from_file(
            ldbws_client,
            "LDBServiceSoap",
            "GetServiceDetails",
            "basic-service-details.xml",
    )
    return ServiceDetails(response)

class TestServiceDetails(object):

    def test_service_details_basics(self, service):
        assert service.generated_at.astimezone(pytz.utc) == \
                datetime.datetime(2016, 8, 6, 21, 15, 22, 396413, tzinfo=pytz.utc)
        assert service.rsid == 'SN101600'
        assert service.service_type == 'train'
        assert service.location_name == 'East Croydon'
        assert service.crs == 'ECR'
        assert service.operator == 'Southern'
        assert service.operator_code == 'SN'
        assert service.cancelled is False
        assert service.cancel_reason is None
        assert service.delay_reason is None
        assert service.overdue_message is None
        assert service.length is None
        assert service.detach_front is False
        assert service.reverse_formation is False
        assert service.platform == "3"
        assert service.sta == "22:33"
        assert service.eta == "On time"
        assert service.ata is None
        assert service.std == "22:33"
        assert service.etd == "On time"
        assert service.atd is None
        assert service.adhoc_alerts is None

    def test_service_details_calling_points(self, service):
        pcps = service.previous_calling_points
        scps = service.subsequent_calling_points

        # Calling Points Lists Lists.
        assert len(pcps) == 1
        assert len(scps) == 1

        pcp = pcps[0]
        scp = scps[0]

        # Calling Points Lists.
        assert len(pcp) == 2
        assert len(scp) == 18

        assert pcp.service_type == None
        assert pcp.change_required == False
        assert pcp.association_is_cancelled == False
        assert scp.service_type == None
        assert scp.change_required == False
        assert scp.association_is_cancelled == False

    def test_service_previous_calling_point(self, service):
        # Test a previous calling point.
        cp = service.previous_calling_points[0][1]

        assert cp.location_name == "Clapham Junction"
        assert cp.crs == "CLJ"
        assert cp.st == "22:23"
        assert cp.et == "On time"
        assert cp.at is None
        assert cp.cancelled is False
        assert cp.length is None
        assert cp.detach_front is False
        assert cp.adhoc_alerts is None

    def test_service_subsequent_calling_points(self, service):
        # Test a subsequent calling point.
        cp = service.subsequent_calling_points[0][1]

        assert cp.location_name == "Three Bridges"
        assert cp.crs == "TBD"
        assert cp.st == "22:53"
        assert cp.et == "On time"
        assert cp.at is None
        assert cp.cancelled is False
        assert cp.length is None
        assert cp.detach_front is False
        assert cp.adhoc_alerts is None



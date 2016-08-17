from .responses import StationBoard

from suds.client import Client
from suds.sax.element import Element

import logging

log = logging.getLogger(__name__)
LDBWS_NAMESPACE = ('com','http://thalesgroup.com/RTTI/2010-11-01/ldb/commontypes')

class Session(object):
    def __init__(self, wsdl=None, api_key=None, timeout=5):

        # Try getting the WSDL and API KEY from the environment if they aren't explicitly passed.
        if not wsdl:
            try:
                wsdl = os.environ['NRE_LDBWS_WSDL']
            except AttributeError:
                raise ValueError("LDBWS WSDL must be either explicitly provided to the Session initializer or via the environment variable NRE_LDBWS_WSDL.")

        if not api_key:
            try:
                api_key = os.environ['NRE_LDBWS_API_KEY']
            except AttributeError:
                raise ValueError("LDBWS API key must be either explicitly provided to the Session initializer or via the environment variable NRE_LDBWS_API_KEY.")

        # Build the SOAP client.
        self._soap_client = Client(wsdl)
        self._soap_client.set_options(timeout=timeout)
        self._service = self._soap_client.service['LDBServiceSoap']

        # Build the SOAP authentication headers.
        access_token = Element('AccessToken', ns=LDBWS_NAMESPACE)
        access_token_value = Element('TokenValue', ns=LDBWS_NAMESPACE)
        access_token_value.setText(api_key)
        access_token.append(access_token_value)
        self._soap_client.set_options(soapheaders=(access_token))

    def get_station_board(self, crs, rows=10, include_departures=True, include_arrivals=False,
            from_filter_crs=None, to_filter_crs=None, time_offset=None, time_window=None):

        # Get the appropriate SOAP query method.
        if include_departures and include_arrivals:
            query = self._service.GetArrivalDepartureBoard
        elif include_departures:
            query = self._service.GetDepartureBoard
        elif include_arrivals:
            query = self._service.GetArrivalBoard
        else:
            raise ValueError("When calling get_station_board, either include_departures or include_arrivals must be set to True.")

        # Construct the query parameters.
        params = {}
        params['crs'] = crs
        params['numRows'] = rows
        if to_filter_crs:
            if from_filter_crs:
                log.warn("get_station_board() can only be filtered on one of from_filter_crs and to_filter_crs. Since both are provided, using only to_filter_crs")
            params['filterCrs'] = to_filter_crs
            params['filterType'] = 'to'
        elif from_filter_crs:
            params['filterCrs'] = from_filter_crs
            params['filterType'] = 'from'
        if time_offset is not None:
            params['timeOffset'] = time_offset
        if time_window is not None:
            params['timeWindow'] = time_window

        # Do the SOAP query.
        # TODO: Some form of error handling.
        soap_response = query(**params)
        return StationBoard(soap_response)



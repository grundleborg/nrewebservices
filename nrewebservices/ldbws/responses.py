from nrewebservices.common import SoapResponseObject
from nrewebservices.common import make_boolean_mapper, make_simple_mapper

def make_nrcc_mapper(field_name):
    def mapper(soap_response):
        try:
            messages = getattr(getattr(soap_response, field_name), 'message')
        except AttributeError:
            messages = []

        return messages
    return mapper

def make_services_mapper(field_name):
    def mapper(soap_response):
        try:
            raw_services = getattr(getattr(soap_response, field_name), 'service')
        except AttributeError:
            raw_services = []

        services = [ServiceItem(raw_service) for raw_service in raw_services]
        return services
    return mapper

def make_services_with_details_mapper(field_name):
    def mapper(soap_response):
        try:
            raw_services = getattr(getattr(soap_response, field_name), 'service')
        except AttributeError:
            raw_services = []

        services = [ServiceItemWithCallingPoints(raw_service) for raw_service in raw_services]
        return services
    return mapper

def make_next_departures_mapper(field_name):
    def mapper(soap_response):
        try:
            raw_departures = getattr(getattr(soap_response, field_name), "destination")
        except AttributeError:
            raw_departures = []

        departures = [DeparturesItem(raw_departure) for raw_departure in raw_departures]
        return departures
    return mapper

def make_next_departures_with_details_mapper(field_name):
    def mapper(soap_response):
        try:
            raw_departures = getattr(getattr(soap_response, field_name), "destination")
        except AttributeError:
            raw_departures = []

        departures = [DeparturesItemWithDetails(raw_departure) for raw_departure in raw_departures]
        return departures
    return mapper

def make_service_locations_mapper(field_name):
    def mapper(soap_response):
        try:
            raw_locations = getattr(getattr(soap_response, field_name), 'location')
        except AttributeError:
            raw_locations = []

        locations = [ServiceLocation(raw_location) for raw_location in raw_locations]
        return locations
    return mapper

def make_calling_points_mapper(field_name):
    def mapper(soap_response):
        try:
            raw_calling_points = getattr(getattr(soap_response, field_name), 'callingPointList')
        except AttributeError:
            raw_calling_points = []

        calling_points = [CallingPoint(raw_calling_point) for raw_calling_point in raw_calling_points]
        return calling_points
    return mapper

class BoardBase(SoapResponseObject):
    """
    This class acts as the base class containing the common attributes for the various classes that
    encapsulate API responses in the form of a list of services at a station. You do not normally
    need to instantiate this class directly.

    Attributes:
        generated_at (datetime): the time at which the board was generated on the LDBWS server.

        location_name (str): the name of the location the board is for.

        crs (str): the CRS code of the location the board is for.

        filter_location_name (str): if a filter was provided in the request, the name of the
            location at which the board services were filtered.

        filter_crs (str): if a filter was provided in the request, the CRS code of the location at
            which the board services were filtered.

        filter_type (str): if a filter was provided in the request, this can contain either "from",
            indicating that the filtered services must have previously called at the filter location
            or "to", indicating that the filtered services must subsequently call at the filter
            location.

        platforms_available (boolean): if true, this indicates that platform information is available
            at this station and can be provided in the user interface. If false, this means that
            platform information is not currently available at this station and should be suppressed
            in the user interface.

        services_available (boolean): if true, this indicates that services are currently available
            in the returned board. If false, this means that services will not be returned in the
            provided board. An example of when this might be set false is when a station has been
            closed due to an incident, but trains are still passing through non-stopping. Normally
            the `nrcc_messages` will contain a message explaining the reason for this when it
            occurs.

        nrcc_messages (list[str]): a list of textual messages that should be displayed with the
            services on the board. These typically contain service information at times when there
            are problems or disruption. They may sometimes contain HTML style <A> an <P> tags.
    """

    field_map = [
            ('generated_at', make_simple_mapper('generatedAt')),
            ('location_name', make_simple_mapper('locationName')),
            ('crs', make_simple_mapper('crs')),
            ('filter_location_name', make_simple_mapper('filterLocationName')),
            ('filter_crs', make_simple_mapper('filterCrs')),
            ('filter_type', make_simple_mapper('filterType')),
            ('platforms_available', make_boolean_mapper('platformAvailable')),
            ('services_available', make_boolean_mapper('areServicesAvailable', True)),
            ('nrcc_messages', make_nrcc_mapper('nrccMessages')),
    ]


class StationBoard(BoardBase):
    field_map = BoardBase.field_map + [
            ('train_services', make_services_mapper('trainServices')),
            ('bus_services', make_services_mapper('busServices')),
            ('ferry_services', make_services_mapper('ferryServices')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(StationBoard, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


class StationBoardWithDetails(BoardBase):
    field_map = BoardBase.field_map + [
            ('train_services', make_services_with_details_mapper('trainServices')),
            ('bus_services', make_services_with_details_mapper('busServices')),
            ('train_services', make_services_with_details_mapper('ferryServices')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(StationBoardWithDetails, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


class NextDeparturesBoard(BoardBase):
    field_map = BoardBase.field_map + [
        ('next_departures', make_next_departures_mapper('departures')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(NextDeparturesBoard, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


class NextDeparturesBoardWithDetails(BoardBase):
    field_map = BoardBase.field_map + [
        ('next_departures', make_next_departures_with_details_mapper('departures')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(NextDeparturesBoardWithDetails, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


class ServiceItemBase(SoapResponseObject):
    field_map = [
            ('origins', make_service_locations_mapper('origin')),
            ('destinations', make_service_locations_mapper('destination')),
            ('current_origins', make_service_locations_mapper('currentOrigins')),
            ('current_destinations', make_service_locations_mapper('currentDestinations')),
            ('sta', make_simple_mapper('sta')),
            ('eta', make_simple_mapper('eta')),
            ('std', make_simple_mapper('std')),
            ('etd', make_simple_mapper('etd')),
            ('platform', make_simple_mapper('platform')),
            ('operator', make_simple_mapper('operator')),
            ('operator_code', make_simple_mapper('operatorCode')),
            ('circular_route', make_boolean_mapper('isCircularRoute')),
            ('cancelled', make_boolean_mapper('isCancelled')),
            ('filter_location_cancelled', make_boolean_mapper('filterLocationCancelled')),
            ('service_type', make_simple_mapper('serviceType')),
            ('length', make_simple_mapper('length')),
            ('detach_front', make_boolean_mapper('detachFront')),
            ('reverse_formation', make_boolean_mapper('isReverseFormation')),
            ('cancel_reason', make_simple_mapper('cancelReason')),
            ('delay_reason', make_simple_mapper('delayReason')),
            ('service_id', make_simple_mapper('serviceID')),
            ('adhoc_alerts', make_simple_mapper('adhocAlerts')),
    ]

    # TODO: Document the properties.


class ServiceItem(ServiceItemBase):
    field_map = ServiceItemBase.field_map + [
            ('rsid', make_simple_mapper('rsid')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(ServiceItem, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


class ServiceItemWithCallingPoints(ServiceItemBase):
    field_map = ServiceItemBase.field_map + [
            ('previous_calling_points', make_calling_points_mapper('previousCallingPoints')),
            ('subsequent_calling_points', make_calling_points_mapper('subsequentCallingPoints')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(ServiceItemWithCallingPoints, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


class ServiceLocation(SoapResponseObject):
    field_map = [
            ('location_name', make_simple_mapper('locationName')),
            ('crs', make_simple_mapper('crs')),
            ('via', make_simple_mapper('via')),
            ('future_change_to', make_simple_mapper('futureChangeTo')),
            ('association_is_cancelled', make_simple_mapper('assocIsCancelled')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(ServiceLocation, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


class CallingPoint(SoapResponseObject):
    field_map = [
            ('location_name', make_simple_mapper('locationName')),
            ('crs', make_simple_mapper('crs')),
            ('st', make_simple_mapper('st')),
            ('et', make_simple_mapper('et')),
            ('at', make_simple_mapper('at')),
            ('cancelled', make_simple_mapper('isCancelled')),
            ('length', make_simple_mapper('length')),
            ('detach_front', make_simple_mapper('detachFront')),
            ('adhoc_alerts', make_simple_mapper('adhocAlerts')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(CallingPoint, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


class NextDeparturesItemBase(SoapResponseObject):
    field_map = [
            ('crs', make_simple_mapper('crs')),
    ]


class NextDeparturesItem(NextDeparturesItemBase):
    field_map = NextDeparturesItemBase.field_map + [
            ('services', make_services_mapper('service')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(NextDeparturesItem, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


class NextDeparturesItemWithCallingPoints(NextDeparturesItemBase):
    field_map = NextDeparturesItemBase.field_map + [
            ('services', make_services_with_details_mapper('service')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(NextDeparturesItemWithCallingPoints, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.


class ServiceDetails(SoapResponseObject):
    field_map = [
            ('generated_at', make_simple_mapper('generatedAt')),
            ('rsid', make_simple_mapper('rsid')),
            ('service_type', make_simple_mapper('serviceType')),
            ('location_name', make_simple_mapper('locationName')),
            ('crs', make_simple_mapper('crs')),
            ('operator', make_simple_mapper('operator')),
            ('operator_code', make_simple_mapper('operatorCode')),
            ('cancelled', make_simple_mapper('isCancelled')),
            ('cancel_reason', make_simple_mapper('cancelReason')),
            ('delay_reason', make_simple_mapper('delayReason')),
            ('overdue_message', make_simple_mapper('overdueMessage')),
            ('length', make_simple_mapper('length')),
            ('detach_front', make_simple_mapper('detachFront')),
            ('reverse_formation', make_simple_mapper('isReverseFormation')),
            ('platform', make_simple_mapper('platform')),
            ('sta', make_simple_mapper('sta')),
            ('eta', make_simple_mapper('eta')),
            ('ata', make_simple_mapper('ata')),
            ('std', make_simple_mapper('std')),
            ('etd', make_simple_mapper('etd')),
            ('atd', make_simple_mapper('atd')),
            ('adhoc_alerts', make_simple_mapper('adhocAlerts')),
            ('previous_calling_points', make_calling_points_mapper('previousCallingPoints')),
            ('subsequent_calling_points', make_calling_points_mapper('subsequentCallingPoints')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(ServiceDetails, self).__init__(soap_response, *args, **kwargs)

    # TODO: Document the properties.



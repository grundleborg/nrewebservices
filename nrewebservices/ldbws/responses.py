from nrewebservices.common import SoapResponseObject
from nrewebservices.common import make_simple_mapper

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
    field_map = [
            ('generated_at', make_simple_mapper('generatedAt')),
            ('location_name', make_simple_mapper('locationName')),
            ('crs', make_simple_mapper('crs')),
            ('filter_location_name', make_simple_mapper('filterLocationName')),
            ('filter_crs', make_simple_mapper('filterCrs')),
            ('filter_type', make_simple_mapper('filterType')),
            ('platform_available', make_simple_mapper('platformAvailable')),
            ('services_available', make_simple_mapper('areServicesAvailable')),
            ('nrcc_messages', make_nrcc_mapper('nrccMessages')),
    ]

    # TODO: Document the properties.


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
            ('circular_route', make_simple_mapper('isCircularRoute')),
            ('cancelled', make_simple_mapper('isCancelled')),
            ('filter_location_cancelled', make_simple_mapper('filterLocationCancelled')),
            ('service_type', make_simple_mapper('service_type')),
            ('length', make_simple_mapper('length')),
            ('detach_front', make_simple_mapper('detachFront')),
            ('reverse_formation', make_simple_mapper('reverse_formation')),
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



from nrewebservices.common import SoapResponseObject
from nrewebservices.common import make_boolean_mapper, make_simple_mapper, make_stripped_text_mapper

def make_nrcc_mapper(field_name):
    def mapper(soap_response):
        try:
            messages = getattr(getattr(soap_response, field_name), 'message')
        except AttributeError:
            messages = []

        return messages
    return mapper

def make_service_mapper(field_name):
    def mapper(soap_response):
        try:
            return ServiceItem(getattr(soap_response, field_name))
        except AttributeError:
            return None

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

def make_service_with_details_mapper(field_name):
    def mapper(soap_response):
        try:
            return ServiceItemWithCallingPoints(getattr(soap_response, field_name))
        except AttributeError:
            return None

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

        departures = [NextDeparturesItem(raw_departure) for raw_departure in raw_departures]
        return departures
    return mapper

def make_next_departures_with_details_mapper(field_name):
    def mapper(soap_response):
        try:
            raw_departures = getattr(getattr(soap_response, field_name), "destination")
        except AttributeError:
            raw_departures = []

        departures = [NextDeparturesItemWithCallingPoints(raw_departure) for raw_departure in raw_departures]
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

def make_calling_point_lists_mapper(field_name):
    def mapper(soap_response):
        try:
            raw_calling_point_lists = getattr(getattr(soap_response, field_name), 'callingPointList')
        except AttributeError:
            raw_calling_point_lists = []

        calling_point_lists = [CallingPointList(calling_point_list) for calling_point_list in raw_calling_point_lists]
        return calling_point_lists
    return mapper

def make_calling_points_mapper(field_name):
    def mapper(soap_response):
        try:
            raw_calling_points = getattr(soap_response, field_name)
        except AttributeError:
            raw_calling_points = []

        calling_points = [CallingPoint(calling_point) for calling_point in raw_calling_points]
        return calling_points
    return mapper

def make_location_text_mapper(field_name):
    def mapper(target):
        try:
            text_items = []
            for i in getattr(target, field_name):
                item_text = i.location_name
                if i.via is not None:
                    item_text += ' ' + i.via
                text_items.append(item_text)
            return ', '.join(text_items)
        except AttributeError:
            return ''
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
            ('filter_crs', make_simple_mapper('filtercrs')),
            ('filter_type', make_simple_mapper('filterType')),
            ('platforms_available', make_boolean_mapper('platformAvailable')),
            ('services_available', make_boolean_mapper('areServicesAvailable', True)),
            ('nrcc_messages', make_nrcc_mapper('nrccMessages')),
    ]


class StationBoard(BoardBase):
    """
    This class represents the arrivals/departures board of a station, provided in response to a
    `get_station_board` request. You do not normally need to instantiate this class directly.

    Attributes:
        train_services (list[ServiceItem]): the list of train services that appear on the requested
            board. This list is provided in the order in which it should be displayed.

        bus_services (list[ServiceItem]): the list of bus services that appear on the requested board.
            This list is provided in the order in which it should be displayed.

        ferry_services (list[ServiceItem]): the list of ferry services that appear on the requested
            board. This list is provided in the order in which it should be displayed.

    Note:
        If you are showing a single combined list of train, bus and ferry services, the sort order
        that is typically used is to sort the services based on scheduled time (arrival/departure as
        appropriate) with the lowest first. Be careful when showing services across midnight.
    """

    field_map = BoardBase.field_map + [
            ('train_services', make_services_mapper('trainServices')),
            ('bus_services', make_services_mapper('busServices')),
            ('ferry_services', make_services_mapper('ferryServices')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(StationBoard, self).__init__(soap_response, *args, **kwargs)


class StationBoardWithDetails(BoardBase):
    """
    This class represents the arrivals/departures board of a station, provided in response to a
    `get_station_board_with_details` request. The difference from `StationBoard` is that this lists
    of services are of type ServiceItemWithCallingPoints, which includes the service calling points,
    which would otherwise have to be requested with individual calls to `get_service_details`. You
    do not normally need to instantiate this class directly.

    Attributes:
        train_services (list[ServiceItemWithCallingPoints]): the list of train services that appear
            on the requested board. This list is provided in the order in which it should be
            displayed.

        bus_services (list[ServiceItemWithCallingPoints]): the list of bus services that appear on
            the requested board. This list is provided in the order in which it should be displayed.

        ferry_services (list[ServiceItemWithCallingPoints]): the list of ferry services that appear
            on the requested board. This list is provided in the order in which it should be
            displayed.

    Note:
        If you are showing a single combined list of train, bus and ferry services, the sort order
        that is typically used is to sort the services based on scheduled time (arrival/departure as
        appropriate) with the lowest first. Be careful when showing services across midnight.
    """

    field_map = BoardBase.field_map + [
            ('train_services', make_services_with_details_mapper('trainServices')),
            ('bus_services', make_services_with_details_mapper('busServices')),
            ('ferry_services', make_services_with_details_mapper('ferryServices')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(StationBoardWithDetails, self).__init__(soap_response, *args, **kwargs)


class NextDeparturesBoard(BoardBase):
    """
    This class represents the board containing the next departures to the requested destinations.
    You do not normally need to instantiate this class directly.

    Attributes:
        next_departures (list[NextDeparturesItem]): a list of objects containing one of the
            requested locations and the next services that depart to that location.
    """
    field_map = BoardBase.field_map + [
        ('next_departures', make_next_departures_mapper('departures')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(NextDeparturesBoard, self).__init__(soap_response, *args, **kwargs)


class NextDeparturesBoardWithDetails(BoardBase):
    """
    This class represents the board containing the next departures to the requested destinations.
    The difference from `NextDeparturesBoard` is that the services returned within the
    `NextDepartureItem`s of this board are of type `NexteDepartureItemWithCallingPoints`, which
    includes the service calling points, which otherwise would have to be requested with individual
    calls to `get_service_details`. You do not normally need to instantiate this class directly.

    Attributes:
        next_departures (list[NextDeparturesItemWithCallingPoints]): a list of objects containing
            one of the requested locations and the next services that depart to that location.
    """
    field_map = BoardBase.field_map + [
        ('next_departures', make_next_departures_with_details_mapper('departures')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(NextDeparturesBoardWithDetails, self).__init__(soap_response, *args, **kwargs)


class ServiceItemBase(SoapResponseObject):
    """
    This class acts as the base class containing the common attributes for the various classes that
    encapsulate individual services as shown on the various boards. You do not normally need to
    instantiate this class directly.

    Attributes:
        origins (list[ServiceLocation]): a list of the origins of this service. Services may have
            multiple origins when they are formed of two separate trains that have been joined
            en-route. This attribute is only populated for boards where arrivals are included.

        destinations (list[ServiceLocation]): a list of the destinations of this service. Services
            may have multiple destinations when they split at a subsequent station into two trains
            to different destinations. This attribute is only populated for boards where departures
            are included.

        current_origins (list[ServiceLocation]): a list of the currently valid origins of the
            service. This attribute is only populated when the scheduled origin(s) have been
            cancelled and the board requsted includes arrivals.

        current_destinations (list[ServiceLocation]): a list of the currently valid destinations of
            the service. This attribute is only populated when the scheduled destination(s) have
            been cancelled and the board requested includes departures.

        sta (str): the scheduled arrival time of the service at this location. The value of the
            field is as outlined in the :ref:`LDBWS Times Section<ldbws-times>`. This field is only
            populated when the board requested includes arrivals and there is an arrival event
            scheduled at this location.

        eta (str): the estimated arrival time of the service at this location. The value of the
            field is as outlined in the :ref:`LDBWS Times Section<ldbws-times>`. This field is only
            populated when the board requested includes arrivals and there is an arrival event
            scheduled at this location.

        std (str): the scheduled departure time of the service at this location. The value of the
            field is as outlined in the :ref:`LDBWS Times Section<ldbws-times>`. This field is only
            populated when the board requested includes departures and there is a departure event
            scheduled at this location.

        etd (str): the estimated departure time of the service at this location. The value of the
            field is as outlined in the :ref:`LDBWS Times Section<ldbws-times>`. This field is only
            populated when the board requested includes departures and there is a departure event
            scheduled at this location.

        platform (str): the platform that this service will use at this location. This will only be
            present where it is available from station CIS systems and where `platforms_available`
            is set to True on the parent board.

        operator (str): the name of the Train Operating Company that operates this service.

        operator_code (str): the two-letter code identifying the Train Operating Company that
            operates this service. Please see the Open Rail Data Wiki `Toc Codes Page 
            <http://nrodwiki.rockshore.net/index.php/TOC_Codes>`_ for the full list.

        circular_route (boolean): when True, this service is operating on a circular route and will
            call at this station again later on its journey. This should be clearly communicated in
            user interfaces to ensure users can effectively identify the right train to take from
            the different options that exist in this case.

        cancelled (boolean): when True, indicates that this service has been cancelled at this
            location.

        filter_location_cancelled (boolean): when True, indicates that the service has had its
            stop at the requested filter location cancelled and now will not stop there.

        service_type (str): the type of transport this service consists of. Can be *train*, *bus* or
            *ferry*.
        
        length (str): the train length (in number of units). If this is set to 0 then the length
            of the train is unknown.

        detach_front (boolean): if True then the service detaches units from the front at this
            location.

        reverse_formation (boolean): if True then the service is operating in reverse formation
            (i.e. the order of the train carriages is the reverse of what it normally is).

        cancel_reason (str): if this service is canelled, the reason for this cancellation.

        delay_reason (str): if this service is delayed, the reason for this delay.

        service_id (str): the unique identifier of this service relative to the station of the board
            at which this service exists. This ID can be used to lookup the service details with
            `get_service_details`. However, this ID is not useful for using with any other API,
            and will expire and stop working within a few hours of the service being deactivated.

        adhoc_alerts (str): a list of adhoc alerts to show for this service at this location.
        
        rsid (str): the Retail Service ID of the service, if known by the Darwin system.

        origin (str): the origin (or origins) of this service as a single string which is suitable
            for display directly to users.

        destination (str): the destination (or destinations) of this service as a single string
            which is suitable for display directly to users.
    """

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
            ('rsid', make_simple_mapper('rsid')),
    ]

    computed_field_map = [
            ('origin', make_location_text_mapper("origins")),
            ('destination', make_location_text_mapper("destinations")),
    ]


class ServiceItem(ServiceItemBase):
    """
    This class represents a single service that appears on an arrival/departure board. You do not
    normally need to instantiate this class directly.
    """

    def __init__(self, soap_response, *args, **kwargs):
        super(ServiceItem, self).__init__(soap_response, *args, **kwargs)


class ServiceItemWithCallingPoints(ServiceItemBase):
    """
    This class represents a single service that appears on an arrival/departure board where details
    were requested. The main difference from a regular `ServiceItem` is that it is prepopulated with
    the previous and subsequent calling points of the service without requiring an additional
    request to `get_service_details` to retrieve these. You do not normally need to instantiate this
    class directly.

    Attributes:
        previous_calling_points ([CallingPointList]): a list of CallingPointList objects on this
            service before the location at which the board was requested. If there is more than one
            CallingPointList, the first list represents the through service, and the subsequent
            lists represent associated services, with the location of the join being the fina
            station on each of the subsequent lists. This is property is only populated when
            requesting an arrivals or arrivals/departures board.

        subsequent_calling_points ([CallingPoint]): a list of CallingPointList objects on this
            service before the location at which the board was requested. If there is more than one
            CallingPointList, the first list represents the through service, and the subsequent
            lists represent associated services, with the location of the join being the final
            station on each of the subsequent lists. This property is only populated when requesting
            a departures or arrivals/departures board.
    """
    field_map = ServiceItemBase.field_map + [
            ('previous_calling_points', make_calling_point_lists_mapper('previousCallingPoints')),
            ('subsequent_calling_points', make_calling_point_lists_mapper('subsequentCallingPoints')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(ServiceItemWithCallingPoints, self).__init__(soap_response, *args, **kwargs)


class ServiceLocation(SoapResponseObject):
    """
    This class represents a single location (station) at which a service either begins or ends. You
    do not normally need to instantiate this class directly.

    Attributes:
        location_name (str): the name of the location.

        crs (str): the CRS code of the location. A CRS code of ??? indicates that the location has
            no CRS code that is known to the Darwin system.

        via (str): when the service is taking an ambiguous route, a string of text describing the
            station or stations it travels via in order to disambiguate. This is typically displayed
            after the destination on departure boards. It is only present for destinations.

        future_change_to (str): if the service is to change to a different mode in future, that mode
            is indicated here (either bus/train/ferry).

        association_is_cancelled (boolean): True if the associated service has been cancelled that
            took this service to this origin or destination, meaning this location will no longer
            be reached by the running service.
    """
    field_map = [
            ('location_name', make_simple_mapper('locationName')),
            ('crs', make_simple_mapper('crs')),
            ('via', make_stripped_text_mapper('via')),
            ('future_change_to', make_simple_mapper('futureChangeTo')),
            ('association_is_cancelled', make_simple_mapper('assocIsCancelled')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(ServiceLocation, self).__init__(soap_response, *args, **kwargs)


class CallingPoint(SoapResponseObject):
    """
    This class represents a single calling point along a service (i.e. a the details of a stop made
    at a station by the service). You do not normally need to instantiate this class directly.

    Attributes:
        location_name (str): the name of the station where the stop occurs.

        crs (str): the CRS code of the station at which the stop occurs. A CRS code of ??? indicates
            that the location has no CRS code that is known to the Darwin system.

        st (str): the scheduled time at which the stop occurs. If this is a previous calling point,
            the value will be the departure time. If it is a subsequent calling point, then the
            value will be an arrival time. The value of this field is as outlined in the section on
            :ref:`LDBWS times<ldbws-times>`.

        et (str): the estimated time at which the service will make this stop. If this is a previous
            calling point, the value will be the departure time. If it is a subsequent calling point
            then the value will be the arrival time. Only one of `et` and `at` is ever populated at
            a time for a given calling point. The value of this field is as outlined in the section
            on :ref:`LDBWS times<ldbws-times>`.

        at (str): the actual time at which the service made this stop. If this is a previous calling
            point, the value will be the departure time. If it is a subsequent calling point then
            the value will be the arrival time. Only one of `et` and `at` is ever populated at a
            time for a given calling point. The value of this field is as outlined in the section on
            :ref:`LDBWS times<ldbws-times>`.

        cancelled (boolean): when True, indicates that this service is cancelled at this location.

        length (str): the train length (in number of units). If this is set to 0 then the length of
            the train is unknown.

        detach_front (boolean): if True then the service detaches units from the front at this
            location.

        adhoc_alerts (str): a list of adhoc alerts to show for this service at this location.
    """
    field_map = [
            ('location_name', make_simple_mapper('locationName')),
            ('crs', make_simple_mapper('crs')),
            ('st', make_simple_mapper('st')),
            ('et', make_simple_mapper('et')),
            ('at', make_simple_mapper('at')),
            ('cancelled', make_boolean_mapper('isCancelled')),
            ('length', make_simple_mapper('length')),
            ('detach_front', make_boolean_mapper('detachFront')),
            ('adhoc_alerts', make_simple_mapper('adhocAlerts')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(CallingPoint, self).__init__(soap_response, *args, **kwargs)


class CallingPointList(SoapResponseObject):
    """
    This class represents a list of calling points along a service. You do not normally need to
    instantiate this class directly.

    Attributes:
        calling_points ([CallingPoint]): the list of calling points this CallingPointList
            represents.

        service_type (str): the type of service these calling points are provided by. Can be either
            'train', 'bus' or 'ferry'.

        change_required (boolean): if True, passengers must change vehicles to access these calling
            points.

        association_is_cancelled (boolean): if True, the association between the service providing
            these calling points and the through service has been cancelled, meaning these calling
            points can no longer be reached on this service.

    Note:
        If a CallingPointList is treated as a regular python list, the calling_points property is
        implicitly accessed.

    """
    field_map = [
            ('calling_points', make_calling_points_mapper('callingPoint')),
            ('service_type', make_simple_mapper('serviceType')),
            ('change_required', make_boolean_mapper('serviceChangeRequired')),
            ('association_is_cancelled', make_boolean_mapper('assocIsCancelled')),
    ]

    def __getitem__(self, item):
        return self.calling_points[item]

    def __len__(self):
        return len(self.calling_points)


class NextDeparturesItemBase(SoapResponseObject):
    """
    This class acts as the base clas for entries on the next departures boards, containing the
    common attributes therof. You do not normally need to instantiate this class directly.

    Attributes:
        crs (str): the CRS code of the location that this departure item contains the next
            departures to.
    """
    field_map = [
            ('crs', make_simple_mapper('_crs')),
    ]


class NextDeparturesItem(NextDeparturesItemBase):
    """
    This class represents an entry on a NextDeparturesBoard, containing the next departures to a
    single location. You do not normally need to instantiate this class directly.

    Attributes:
        service (ServiceItem): the next service to depart to the requested location.
    """
    field_map = NextDeparturesItemBase.field_map + [
            ('service', make_service_mapper('service')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(NextDeparturesItem, self).__init__(soap_response, *args, **kwargs)


class NextDeparturesItemWithCallingPoints(NextDeparturesItemBase):
    """
    This class represents an entry on a NextDeparturesBoardWithDetails, containing the next
    departures to a single location. The difference between this and `NextDeparturesItem` is that
    the services are of type `ServiceItemWithCallingPoints`, which includes the service calling
    points which otherwise would have to be requested with individual calls to
    `get_service_details`. You do not normally need to instantiate this class directly.

    Attributes:
        service (ServiceItemWithCallingPoints): the next service to depart to the requested
            location.
    """
    field_map = NextDeparturesItemBase.field_map + [
            ('service', make_service_with_details_mapper('service')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(NextDeparturesItemWithCallingPoints, self).__init__(soap_response, *args, **kwargs)


class ServiceDetails(SoapResponseObject):
    """
    This class represents the details of a service from the point of view of the station at which
    that service was requested. You do not normally need to instantiate this class directly.

    Attributes:
        generated_at (datetime): the time at which the service details were generated on the LDBWS
            server.
        
        rsid (str): the Retail Service ID of the service, if known by the Darwin system.

        service_type (str): The type of service ("bus/ferry/train"). Note that real-time information
            such as estimated and actual times and cancellations is only available for train
            services.

        location_name (str): the name of the location at which this service was requested. This is
            determined by the board that the service ID was originally retrieved from. All other
            fields in this object are from the point of view of inspecting the service at this
            location.

        crs (str): the CRS code of the location at which this service was requested. See the
            `location_name` attribute for more details.

        operator (str): the name of the Train Operating Company that operates this service.

        operator_code (str): the two-letter code identifying the Train Operating Company that
            operates this service. Please see the Open Rail Data Wiki `Toc Codes Page 
            <http://nrodwiki.rockshore.net/index.php/TOC_Codes>`_ for the full list.

        cancelled (boolean): when True, indicates that this service has been cancelled at this
            location.

        cancel_reason (str): if this service is canelled, the reason for this cancellation.

        delay_reason (str): if this service is delayed, the reason for this delay.

        overdue_message (str): if a report on an expected movement of this service has not been
            received on time, this attribute will contain a plain-English explanation of the report
            which was expected.

        length (str): the train length (in number of units). If this is set to 0 then the length
            of the train is unknown.

        detach_front (boolean): if True then the service detaches units from the front at this
            location.

        reverse_formation (boolean): if True then the service is operating in reverse formation
            (i.e. the order of the train carriages is the reverse of what it normally is).

        platform (str): the platform that this service will use at this location. This will only be
            present where it is available from station CIS systems and where `platforms_available`
            is set to True on the board from which this service was requested.

        sta (str): the scheduled arrival time of the service at this location. The value of the
            field is as outlined in the :ref:`LDBWS Times Section<ldbws-times>`. This field is only
            populated when the board requested includes arrivals and there is an arrival event
            scheduled at this location.

        eta (str): the estimated arrival time of the service at this location. The value of the
            field is as outlined in the :ref:`LDBWS Times Section<ldbws-times>`. This field is only
            populated when there is an arrival event scheduled at this location. Only one of `eta`
            and `ata` will be present at a time for a given service.

        ata (str): the actual arrival time of the service at this location. The value of the
            field is as outlined in the :ref:`LDBWS Times Section<ldbws-times>`. This field is only
            populated when there is an arrival event scheduled at this location. Only one of `eta`
            and `ata` will be present at a time for a given service.

        std (str): the scheduled departure time of the service at this location. The value of the
            field is as outlined in the :ref:`LDBWS Times Section<ldbws-times>`. This field is only
            populated when the board requested includes departures and there is a departure event
            scheduled at this location.

        etd (str): the estimated departure time of the service at this location. The value of the
            field is as outlined in the :ref:`LDBWS Times Section<ldbws-times>`. This field is only
            populated when there is a departure event scheduled at this location. Only one of `etd`
            and `atd` will be present at a time for a given service.

        atd (str): the actual departure time of the service at this location. The value of the
            field is as outlined in the :ref:`LDBWS Times Section<ldbws-times>`. This field is only
            populated when there is a departure event scheduled at this location. Only one of `etd`
            and `atd` will be present at a time for a given service.

        adhoc_alerts (str): a list of adhoc alerts to show for this service at this location.

        previous_calling_points ([CallingPointList]): a list of CallingPointList objects on this
            service before the location at which the board was requested. If there is more than one
            CallingPointList, the first list represents the through service, and the subsequent
            lists represent associated services, with the location of the join being the final
            station on each of the subsequent lists.

        subsequent_calling_points ([CallingPointList]): a list of CallingPointList objects on this
            service after the location at which the board was requested. If there is more than one
            CallingPointList, the first list represents the through service, and the subsequent
            lists represent associated services, with the location of the join being the first
            station on each of the subsequent lists.
    """
    field_map = [
            ('generated_at', make_simple_mapper('generatedAt')),
            ('rsid', make_simple_mapper('rsid')),
            ('service_type', make_simple_mapper('serviceType')),
            ('location_name', make_simple_mapper('locationName')),
            ('crs', make_simple_mapper('crs')),
            ('operator', make_simple_mapper('operator')),
            ('operator_code', make_simple_mapper('operatorCode')),
            ('cancelled', make_boolean_mapper('isCancelled')),
            ('cancel_reason', make_simple_mapper('cancelReason')),
            ('delay_reason', make_simple_mapper('delayReason')),
            ('overdue_message', make_simple_mapper('overdueMessage')),
            ('length', make_simple_mapper('length')),
            ('detach_front', make_boolean_mapper('detachFront')),
            ('reverse_formation', make_boolean_mapper('isReverseFormation')),
            ('platform', make_simple_mapper('platform')),
            ('sta', make_simple_mapper('sta')),
            ('eta', make_simple_mapper('eta')),
            ('ata', make_simple_mapper('ata')),
            ('std', make_simple_mapper('std')),
            ('etd', make_simple_mapper('etd')),
            ('atd', make_simple_mapper('atd')),
            ('adhoc_alerts', make_simple_mapper('adhocAlerts')),
            ('previous_calling_points', make_calling_point_lists_mapper('previousCallingPoints')),
            ('subsequent_calling_points', make_calling_point_lists_mapper('subsequentCallingPoints')),
    ]

    def __init__(self, soap_response, *args, **kwargs):
        super(ServiceDetails, self).__init__(soap_response, *args, **kwargs)



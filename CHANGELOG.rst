----------
Change Log
----------

v0.2.1-dev
==========


v0.2.0
======

* Discontinue support for Python 2.6 and 3.3, and officially add support for Python 3.6 & 3.7.
* Update to the 2017-10-01 version of the LDBWS schema. This introduces Formations for services.

v0.1.4
======

* Convenience properties of board services *origin* and *destination* which provide a single string
  suitable for display directly to users, instead of a list of objects.
* Strip whitespace from `via` field.
* Python 3.6 support.
* Break CallingPointList out into an object, as the list itself has properties too.

v0.1.3
======

* Fresh release due to messing up v0.1.2 upload to PyPI.

v0.1.2
======

* Fix exception when getting LDBWS WSDL or API KEy from environment variables.
* Fix BoardBase.filter_crs property mapping so it is now correctly populated.
* Fix python 2.6 compatability.
* Extra check in get_[fastest|next]_departures[_with_details] methods to ensure that the
  destinations parameter is actually a list.

v0.1.1
======

* Improved test coverage for LDBWS.
* Fix a bug where the ferry services overwrote the train services in StationBoardWithDetails
  objects.
* Move rsid from ServiceItem to ServiceItemBase as ServiceItemWithCallingPoints does have this
  property too, even though the official documentation claims otherwise.
* Fix bug where ServiceItemWithCallingPoints did not have the double-nesting of calling points lists
  and also fix the mapper generator for decoding these lists-of-lists.
* Fix default values of CallingPoint detach_front and cancelled properties (should return False when
  not present in the web service response).
* Fix default values of ServiceDetails reverse_formation, cancelled and detach_front to be False.

v0.1.0
======

* Initial release.
* Complete basic API for the LDBWS web service.



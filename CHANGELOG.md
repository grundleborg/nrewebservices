v0.1.2-dev
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



v0.1.1-dev
==========

* Improved test coverage for LDBWS.
* Fix a bug where the ferry services overwrote the train services in StationBoardWithDetails
  objects.
* Move rsid from ServiceItem to ServiceItemBase as ServiceItemWithCallingPoints does have this
  property too, even though the official documentation claims otherwise.

v0.1.0
======

* Initial release.
* Complete basic API for the LDBWS web service.



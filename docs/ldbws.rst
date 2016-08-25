Live Departure Boards
=====================

Overview
--------

The ldbws module provides an API for querying the Darwin OpenLDBWS web service. This web service
allows for querying all the basic information provided via station departure boards, and is suitable
for building applications which replicate some or all of this functionality. For more involved
projects, especially those where you wish to combine web service data with data from the Darwin Push
Port, the :doc:`LDBWS Staff Version <staff>` web service may be more appropriate due to the extra
fields it provides on response objects.

Official Documentation
----------------------

The official documentation can be
`found here <https://lite.realtime.nationalrail.co.uk/openldbws/>`_. Whilst a useful resource for
the more experienced developer, experience has shown this page to be somewhat lacking, and even
entirely incorrect at times. This library provides detailed documentation of the individual API
calls and the response object properties, derived from the official documentation, but augmented
with additional explanations and corrections where necessary.

This library also provides a number of convenience functions which perform commonly needed
transformations on the raw data returned by the web service to make life easier for developers.

Getting an Access Token
-----------------------

In order to access the web service, you will need to sign up for an access token from National Rail
Enquiries `here <http://realtime.nationalrail.co.uk/OpenLDBWSRegistration>`_. To do this you are
required to sign the NRE Open Data license. You should note in particular the usage caps and charges
for high usage. As a convenience,  methods which generatecalls to the web service that count towards
usage caps or charges are clearly indicated in this calls to the web service that count towards
usage caps or charges are clearly indicated in this documentation. However the accuracy of this
information cannot be guaranteed, so if you are concerned about usage caps or charges you should
make your own investigations to check.

Web Service Sessions
--------------------

Interaction with the LDBWS API takes place through an instance of the
:py:obj:`Session <nrewebservices.ldbws.Session>` object. On instantiating the Session, the WSDL
for the web service is retrieved and parsed. This requires a series of files to be retrieved from
the LDBWS server, and so will take some time to return (typically this takes around 1-2 seconds
from an internet connected server). The WSDL is then parsed and cached for the life of the Session
object ensuring subsequent API requests can take place immediately.

Once the :py:obj:`Session <nrewebservices.ldbws.Session>` object has been instantiated, API requests
are made by means of calling the available methods on this object.


.. _ldbws-times:

Times
-----

Many of the objects returned by the LDBWS API contain attributes which represent times. However, in
the raw API these are treated as strings, because there are some values they can contain which are
not valid times. In general, times are provided in the format hh:mm. However, sometimes they may
be followed by an asterisk indicating that the Darwin system is unsure as to their reliability.
They may also be replaced in some cases by strings which can include the following "Delayed", 
"On Time", "Cancelled" and "No report". The values of these fields are sutiable to be displayed
directly as provided on departure boards (in fact, that is what the on-platform ones at stations
do). However, if you are planning to parse them as times, you should take these alternative values
into consideration.

Usage Example
-------------

See the file *examples/ldbws.py* in this repository for a simple usage example.

API Reference
-------------

For details of all the methods available on the `Session` object, as well as the response objects
and their properties, please see the :doc:`LDBWS API Reference <api-ldbws>`.



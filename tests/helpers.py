import os
import pytest

def base_path():
    return os.path.dirname(os.path.abspath(__file__))

def mock_ldbws_response_from_file(client, op1, op2, filename=None):
    # Read the XML file.
    file_path = os.path.abspath(os.path.join(base_path(), 'data/ldbws', filename))
    f = open(file_path, 'r')
    xml_content = f.read()
    f.close()
    xml_content = xml_content.encode('utf-8')

    # Inject the fake message reply to a suds request context.
    request_context = client.service[op1][op2](__inject={'msg': xml_content, 'reply': xml_content})
    return request_context.process_reply(xml_content)

def ldbws_client_helper():
    # Import suds client.
    from suds.client import Client
    
    # Build the absolute path to the local copy of the WSDL as urllib2 doesn't support relative
    # paths for accessing local files.
    wsdl = "file://" + os.path.abspath(os.path.join(base_path(), "wsdl/ldbws/", "wsdl.aspx"))
    
    # Instantiate the soap client.
    client = Client(wsdl, nosend=True)

    return client



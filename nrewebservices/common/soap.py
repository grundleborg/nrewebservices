class SoapResponseObject(object):
    
    def __init__(self, soap_response):
        for field, mapper in self.__class__.field_map:
            value = mapper(soap_response)
            setattr(self, field, value)

        if hasattr(self.__class__, 'computed_field_map'):
            for field, mapper in self.__class__.computed_field_map:
                value = mapper(self)
                setattr(self, field, value)


def make_simple_mapper(field_name):
    def mapper(soap_response):
        try:
            value = getattr(soap_response, field_name)
        except AttributeError:
            value = None

        return value
    return mapper

def make_boolean_mapper(field_name, default=False):
    def mapper(soap_response):
        try:
            value = getattr(soap_response, field_name)
        except AttributeError:
            value = default

        return value
    return mapper

def make_stripped_text_mapper(field_name):
    def mapper(soap_response):
        try:
            value = getattr(soap_response, field_name).strip()
        except AttributeError:
            value = None

        return value
    return mapper



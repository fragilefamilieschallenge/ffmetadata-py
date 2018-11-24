"""
Python wrapper for the Fragile Families Metadata API.

Examples
--------
>>> import ff

# Get all attributes of a variable
>>> ff.select('ce3datey')  # doctest:+ELLIPSIS
{'data_source': 'constructed', 'data_type': 'Continuous', ...

# Get a single attribute of a variable
>>> ff.select('ce3datey', 'data_source')
'constructed'

# Get multiple attributes of a variable
>>> ff.select('ce3datey', ['name', 'data_source'])
{'data_source': 'constructed', 'name': 'ce3datey'}

# Find variable(s) where name='ce3datey'
>>> ff.search({'name': 'name', 'op': 'eq', 'val': 'ce3datey'})
['ce3datey']

# Find variable(s) where data_source='constructed' AND name ends with 'e'
>>> ff.search([{'name': 'data_source', 'op': 'eq', 'val': 'constructed'}, {'name': 'name', 'op': 'like', 'val': '%e'}])  # doctest:+ELLIPSIS
['cf1age', 'cf1ethrace', ...

# Find variable(s) where data_source='constructed' OR name starts with 'c' OR name ends with 'd'
>>> ff.search({'or': [{'name': 'data_source', 'op': 'eq', 'val': 'constructed'}, {'name': 'name', 'op': 'like', 'val': 'c%'}, {'name': 'name', 'op': 'like', 'val': '%d'}]})  # doctest:+ELLIPSIS
['cf1intmon', 'cf1intyr', ...

# Find variable(s) where data_source='constructed' OR (name ends with 'f' AND data_source='questionnaire')
>>> ff.search({'or': [{'name': 'data_source', 'op': 'eq', 'val': 'constructed'}, {'and': [{'name': 'name', 'op': 'like', 'val': '%f'}, {'name': 'data_source', 'op': 'eq', 'val': 'questionnaire'}]}]})  # doctest:+ELLIPSIS
['cf1intmon', 'cf1intyr', ...

"""

import json
import urllib
import requests

__version__ = '1.1.0'
name = "ffmetadata-py"
BASE_URL = 'http://api.metadata.fragilefamilies.princeton.edu'


def select(var_name, attr_name=None):
    """
    Return attribute(s) of a variable given the variable name and an optional field name, or list of attribute name(s)
    :param var_name: Name of the variable we're interested in.
    :param attr_name: A string representing the name of the attribute whose value we want to fetch. This can also be
        a list of strings in case of multiple attributes. If None, all attributes of the variable are returned.
    :return: A dictionary of attribute => value mappings if multiple attributes were requested (i.e. attr_name is a
        list), or a string value if a single attribute name was requested (i.e. attr_name is a string)
    """
    single = isinstance(attr_name, str)
    if attr_name is not None:
        if single:
            params = {attr_name: attr_name}
        else:
            params = dict([(f, f) for f in attr_name])
    else:
        params = None

    endpoint = 'variable/%s' % var_name
    data = _get(endpoint, params)

    return data[attr_name] if single else data


def search(filters=None):
    """
    Search for variable names given a list or dictionary of 'filter(s)'.
    A 'filter' is defined as a dictionary with keys 'name','op','val' representing the attribute name, a comparison
    operator, and the value for comparison.
    If multiple filters are specified as a list, they're combined using the AND operator.
    Filters can also be specified as a dictionary, keyed with 'and' or 'or', and the values being a list of individual
    'filters'.

    See examples of usage in this module. Note that this function doesn't do any advanced processing whatsoever, but
    passes on the filters 'as-is' to the server.

    :param filters: A list of filters, or a dictionary with key 'and' or 'or', and the values as a list of filters.
    :return: A list of variable names corresponding to the search criteria.
    """
    filters = filters or []
    query_string_dict = {'filters': filters}
    query_string = urllib.parse.quote(json.dumps(query_string_dict))
    return _get('variable?q=%s' % query_string)


def _get(endpoint, params=None):
    """Return a dictionary of attribute => value mapping for JSON results
    obtained at a specified endpoint, with optional query parameters.
    Raises SystemError on 5xx responses or RuntimeError on 4xx responses
    """
    url = '%s/%s' % (BASE_URL, endpoint)
    url = requests.Request('GET', url, params=params).prepare().url
    response = requests.get(url)

    if 500 <= response.status_code < 600:
        raise SystemError("Internal Error on Server")

    d = response.json()
    if 400 <= response.status_code < 500:
        raise RuntimeError(d['message'])
    return d


if __name__ == "__main__":
    import doctest
    doctest.testmod()

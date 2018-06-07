"""============================================================================
Python wrapper for the Fragile Families Metadata API.

Examples
--------
>>> import ff
>>> data = ff.select('cm1relf')
>>> data = ff.filter(responses='sometimes')
>>> data = ff.search('age', 'label')
============================================================================"""

import requests

# -----------------------------------------------------------------------------

BASE_URL = 'http://api.metadata.fragilefamilies.princeton.edu'


# -----------------------------------------------------------------------------

def select(var_name, field_name=None):
    """Returns dictionary of metadata for variable `var_name`. Provided an
    optional `field_name`, return only data for the specified field.
    """
    params = {'varName': var_name}
    if field_name:
        params['fieldName'] = field_name
    return _get('select', params)


# -----------------------------------------------------------------------------

def filter(**kwargs):
    """Return a list of variables where each field name matches the provided
    value.
    """
    params = dict(kwargs)
    return _get('filter', params)['matches']


# -----------------------------------------------------------------------------

def search(query, field_name):
    """Return a list of variables where `query` is found in `field_name`.
    """
    params = {'query': query, 'fieldName': field_name}
    return _get('search', params)['matches']


# -----------------------------------------------------------------------------

def _get(endpoint, params):
    """Return JSON as dictionary based on endpoint and query parameters.
    """
    url = '%s/%s' % (BASE_URL, endpoint)
    url = requests.Request('GET', url, params=params).prepare().url
    response = requests.get(url)
    if response.status_code == 500:
        raise ConnectionError(response.reason)
    json = response.json()
    if 'error code' in json:
        raise AttributeError(json['error_description'])
    return json

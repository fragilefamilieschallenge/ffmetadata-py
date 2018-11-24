[![PyPI version](https://badge.fury.io/py/ffmetadata-py.svg)](https://pypi.org/project/ffmetadata-py/)

# ffmetadata-py
Python wrapper for Fragile Families Metadata API

This Python package provides convenient wrappers to interface with the [Fragile Families Metadata API](https://github.com/fragilefamilieschallenge/metadata_app). By downloading and importing the `ff` module, users can query the metadata variables. No other software installation is necessary.

Requirements
------------

The `ff` module has been tested on Python 3.6, and should work on most Python 3.x installations.

Installation
------------

The easiest way to install and use the module is to do a `pip install`

```
pip install ffmetadata-py
```

This step will also install any dependencies if needed (currently, the `requests` and `simplejson` libraries).

Alternatively, you can clone this Github repository and place the `ff` folder and it's contents at a location accessible by your Python 3 installation (most commonly the `site-packages` folder for your Python installation). In this scenario, make sure that you have recent versions of the `requests` and `simplejson` libraries installed.

Getting Started
---------------

To get started, import the ff module using `import ff`. Follow the examples below on how to use the library.

Examples
--------

### Getting attributes of a variable

#### Get *all* attributes of a variable
Given the variable name, this function call returns a dictionary of all attribute name/value pairs.
```
>>> ff.select('ce3datey')
{'data_source': 'constructed', 'data_type': 'Continuous', ...
```

#### Get a single attribute of a variable
To get a single attribute value, call the `select` function with the second argument as the attribute you're interested in. Most attributes return `str` values, but a handful have `int` return values.
```
>>> ff.select('ce3datey', 'data_source')
'constructed'
```

#### Get multiple attributes of a variable
To get multiple attribute values, call the `select` function with the second argument as a list of string attribute names. A dictionary with name/value pairs is returned.
```
>>> ff.select('ce3datey', ['name', 'data_source'])
{'data_source': 'constructed', 'name': 'ce3datey'}
```

### Searching for variables
Querying variables is done using the `search` function. In the simplest case, this function expects a dictionary with keys *name*, *op* and *val*. In all cases, a list of variable names is returned. Some examples follow.

#### Find variable(s) where name='ce3datey'
```
>>> ff.search({'name': 'name', 'op': 'eq', 'val': 'ce3datey'})
['ce3datey']
```

#### Find variable(s) where data_source='constructed' AND name ends with 'e'
Multiple search criteria can be specified by passing in a list of dictionaries. These are combined with an `AND` clause.
```
>>> ff.search([{'name': 'data_source', 'op': 'eq', 'val': 'constructed'}, {'name': 'name', 'op': 'like', 'val': '%e'}])
['cf1age', 'cf1ethrace', ...
```

#### Find variable(s) where data_source='constructed' OR name starts with 'c' OR name ends with 'd'
To specify an `OR` clause for multiple search combination, replace the search criteria with a dictionary keyed by `OR`, with values as a list of dictionaries.
```
>>> ff.search({'or': [{'name': 'data_source', 'op': 'eq', 'val': 'constructed'}, {'name': 'name', 'op': 'like', 'val': 'c%'}, {'name': 'name', 'op': 'like', 'val': '%d'}]})
['cf1intmon', 'cf1intyr', ...
```

#### Find variable(s) where data_source='constructed' OR (name ends with 'f' AND data_source='questionnaire')
More complicated search queries can b constructed, by combining several AND/OR clauses. In such cases, at any point where you want to specify a sub-query, pass in a dictionary keyed by either an `AND` or `OR`, with the values being valid search criteria themselves - either dictionaries of name/op/val keys, or sub-queries (defined recursively).
```
>>> ff.search({'or': [{'name': 'data_source', 'op': 'eq', 'val': 'constructed'}, {'and': [{'name': 'name', 'op': 'like', 'val': '%f'}, {'name': 'data_source', 'op': 'eq', 'val': 'questionnaire'}]}]})
['cf1intmon', 'cf1intyr', ...
```

For more complicated search queries, you may find the interactive [Advanced Search](http://metadata.fragilefamilies.princeton.edu/search) page on the project website useful.

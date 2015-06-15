# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six
import json
import pyparsing as pp
from . import grammar

__all__ = ['loads', 'dumps']


def loads(query):
    """
    Converts a GraphQL string into a Python dictionary.

    >>> graphql.loads(\"\"\"
    {
        user(id: 232) {
            id,
            name
        }
    }
    \"\"\")

    [
        {
            "name": "user",
            "params": {"id": 232},
            "properties": [
                {"name": "id"},
                {"name": "name"}
            ]
        }
    ]
    """
    
    data = []

    for parsed_obj in grammar.root.parseString(query):
        data.append(load_obj(parsed_obj))

    return data


def dumps(ast, compact=False, indent=2):
    """
    Converts a Python dict representing a GraphQL structure to
    its string form. The `compact` argument is a shorthand for `indent=0`,
    so `graphql.dumps(x, compact=True) == graphql.dumps(x, indent=0)`.

    >>> graphql.dumps([
        {
            "name": "user",
            "params": {"id": 232},
            "properties": [
                {"name": "id"},
                {"name": "name"}
            ]
        }
    ], indent=4)

    {
        user(id: 232) {
            id,
            name
        }
    }
    """
    
    if compact:
        indent = 0
    
    chunks = ['{']
    if indent > 0:
        chunks.append('\n')

    for obj in ast:
        chunks.extend(dump_object(obj, indent))
        chunks.append(',\n\n' if indent > 0 else ',')

    chunks.pop(-1)  # remove the last comma
    if indent > 0:
        chunks.append('\n')
    chunks.append('}')

    return ''.join(chunks)


def dump_object(obj, indent, indent_level=1):
    """
    Converts a python object to a GraphQL string
    """
    
    is_compact = indent == 0
    chunks = [] if is_compact else [' ' * indent * indent_level]

    chunks.append(obj['name'])

    if 'params' in obj:
        chunks.extend(dump_params(obj['params'], is_compact))

    if 'filters' in obj:
        for filter_name, params in iter(obj['filters'].items()):
            chunks.extend(['.', filter_name])
            chunks.extend(dump_params(params, is_compact))

    if 'properties' in obj:
        chunks.append('{' if is_compact else ' {\n')

        for prop in obj['properties']:
            chunks.extend(dump_object(prop, indent, indent_level + 1))
            chunks.append(',' if is_compact else ',\n')

        chunks.pop(-1)  # remove the last comma
        if is_compact:
            chunks.append('}')
        else:
            chunks.extend(['\n', ' ' * indent * indent_level, '}'])

    return chunks


def dump_params(params, compact):
    """
    Converts list of params to a GraphQL representation.
    """
    
    SEP = ': ' if not compact else ':'

    if not isinstance(params, dict):
        return ['(', json.dumps(params), ')']

    chunks = ['(']
    for k, v in iter(params.items()):
        chunks.extend([k, SEP, json.dumps(v)])
    chunks.append(')')
    
    return chunks


def load_obj(parsed_obj):
    """
    Converts a parsed GraphQL object into a Python dict
    """
    
    name, params, filters = get_header(parsed_obj)
    properties = get_properties(parsed_obj)

    obj = {'name': name}
    if params:
        obj['params'] = load_args(params)

    if filters:
        obj['filters'] = [(filter_[0], load_args(filter_[1:]))
                           for filter_ in filters]

    obj['properties'] = []
    for p in properties:
        if isinstance(p, pp.ParseResults):
            obj['properties'].append(load_obj(p))
        else:
            obj['properties'].append({'name': p})

    return obj


def load_args(args):
    """
    Converts parsed values inside parens into its Python equivalents.
    """
    
    if len(args) == 1 and isinstance(args[0], six.string_types):
        return json.loads(args[0])

    parsed_args = {}
    for arg in args:
        if not isinstance(arg, list):
            arg = arg.asList()

        param = arg[0]
        arguments = arg[1:]
        parsed_args[param] = json.loads(arguments[0])

    return parsed_args


def get_header(obj):
    header, _ = obj
    name = header[0]

    return name, header.get('params', []), header.get('filters', [])


def get_properties(obj):
    _, properties = obj

    return properties

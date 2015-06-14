# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import ast
import six
import pyparsing as pp
from . import grammar

__all__ = ['loads', 'dumps']


def loads(query):
    data = []

    for parsed_obj in grammar.root.parseString(query):
        data.append(load_obj(parsed_obj))

    return data


def dumps(ast, indent=0):
    # A cada nó, antes de adicionar,
    # deve checar com a gramática se é permitido!
    return '{%s}' % doc


def load_obj(parsed_obj):
    name, params, filters = get_header(parsed_obj)
    properties = get_properties(parsed_obj)

    obj = {'name': name}
    if params:
        obj['params'] = load_args(params)

    if filters:
        obj['filters'] = load_args(filters)

    obj['properties'] = []
    for p in properties:
        if isinstance(p, pp.ParseResults):
            obj['properties'].append(load_obj(p))
        else:
            obj['properties'].append({'name': p})

    return obj


def load_args(args):
    if len(args) == 1 and isinstance(args[0], six.string_types):
        return convert_literal(args[0])

    parsed_args = {}
    for arg in args:
        arg = arg.asList()
        param = arg[0]
        arguments = arg[1:]

        if len(arguments) == 1 and not isinstance(arguments[0], list):
            parsed_args[param] = convert_literal(arguments[0])
        else:
            parsed_args[param] = dict((k, convert_literal(v))
                                      for k, v in arguments)

    return parsed_args


def convert_literal(l):
    return ast.literal_eval({
        "null": "None",
        "true": "True",
        "false": "False"
    }.get(l, l))


def get_header(obj):
    header, _ = obj
    name = header[0]

    return name, header.get('params', []), header.get('filters', [])


def get_properties(obj):
    _, properties = obj

    return properties

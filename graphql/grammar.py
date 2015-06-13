# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pyparsing as pp


def set_debug(debug):
    root.setDebug(debug)


OPEN_BRACE = pp.Suppress('{')
CLOSE_BRACE = pp.Suppress('}')
OPEN_PAREN = pp.Suppress('(')
CLOSE_PAREN = pp.Suppress(')')
COMMA = pp.Suppress(',')
COLON = pp.Suppress(':')
DOT = pp.Suppress('.')
EOF = pp.Suppress(pp.LineEnd())

identifier = pp.Regex(r'[a-zA-Z_][a-zA-Z0-9_/]*').setName('identifier')

string = pp.quotedString.setName('quoted string')
number = pp.Regex(r'-?\d+(\.\d+)?').setName('number')
literal = (number | string | "null" | "true" | "false").setName('literal')

param = pp.Group(identifier + COLON + literal).setName('param')
param_pairs_list = (param + pp.ZeroOrMore(COMMA + param))
params_list = ( OPEN_PAREN
              + pp.Optional(literal | param_pairs_list)
              + CLOSE_PAREN).setName('params list')

filter_param = pp.Group(identifier + params_list).setName('filter param')

gql_header = ( identifier
             + pp.Optional(pp.Group(params_list).setResultsName('params'))
             + pp.Group(pp.ZeroOrMore(DOT + filter_param)).setResultsName('filters'))

gql_object = pp.Forward()
gql_property = pp.Group(gql_object) | identifier
gql_properties_list = gql_property + pp.ZeroOrMore(COMMA + gql_property)
gql_object << ( pp.Group(gql_header).setResultsName('header')
              + OPEN_BRACE
              + pp.Group(gql_properties_list).setResultsName('properties')
              + CLOSE_BRACE)

gql_objects_list = pp.Group(gql_object) + pp.ZeroOrMore(COMMA + pp.Group(gql_object))
root = pp.Suppress(pp.LineStart()) + OPEN_BRACE + gql_objects_list + CLOSE_BRACE + EOF

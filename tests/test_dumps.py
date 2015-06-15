# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from textwrap import dedent
import graphql


def test_simple_dumps():
    query = graphql.dumps([
        {
            "name": "user",
            "params": 232,
            "properties": [
                {"name": "id"},
                {"name": "name"}
            ]
        }
    ], indent=4)

    expected = """{
    user(232) {
        id,
        name
    }
}"""

    assert query == expected


def test_dumps_with_filters():
    query = graphql.dumps([
        {
            "name": "user",
            "params": 232,
            "filters": {"active": True},
            "properties": [
                {"name": "id"},
                {"name": "name"}
            ]
        }
    ], indent=4)

    expected = """{
    user(232).active(true) {
        id,
        name
    }
}"""

    assert query == expected


def test_dumps_with_named_args():
    query = graphql.dumps([
        {
            "name": "user",
            "params": {"id": 232},
            "properties": [
                {"name": "id"},
                {"name": "name"}
            ]
        }
    ], indent=4)

    expected = """{
    user(id: 232) {
        id,
        name
    }
}"""

    assert query == expected


def test_dumps_nested_objects():
    query = graphql.dumps([
        {
            "name": "user",
            "params": {"id": 232},
            "properties": [
                {"name": "id"},
                {"name": "name"},
                {
                    "name": "photo",
                    "params": {"size": 50},
                    "properties": [
                        {"name": "url"},
                        {"name": "width"},
                        {"name": "height"}
                    ]
                }
            ]
        }
    ], indent=4)

    expected = """{
    user(id: 232) {
        id,
        name,
        photo(size: 50) {
            url,
            width,
            height
        }
    }
}"""

    assert query == expected


def test_dumps_multiple_objects():
    query = graphql.dumps([
        {
            "name": "user",
            "params": {"id": 232},
            "properties": [
                {"name": "id"},
                {"name": "name"},
            ]
        },
        {
            "name": "photo",
            "params": {"size": 50},
            "properties": [
                {"name": "url"},
                {"name": "width"},
                {"name": "height"}
            ]
        }
    ], indent=4)

    expected = """{
    user(id: 232) {
        id,
        name
    },

    photo(size: 50) {
        url,
        width,
        height
    }
}"""

    assert query == expected


def test_dumps_compact():
    query = graphql.dumps([
        {
            "name": "user",
            "params": {"id": 232},
            "properties": [
                {"name": "id"},
                {"name": "name"},
            ]
        },
        {
            "name": "photo",
            "params": {"size": 50},
            "properties": [
                {"name": "url"},
                {"name": "width"},
                {"name": "height"}
            ]
        }
    ], compact=True)

    assert query == ('{user(id:232){id,name},'
                      'photo(size:50){url,width,height}}')

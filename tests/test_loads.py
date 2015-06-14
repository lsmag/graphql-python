# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import graphql


def test_load_simple_object():
    assert graphql.loads("""
    {
        user {
            id,
            name
        }
    }""") == [
        {
            "name": "user",
            "properties": [
                {"name": "id"},
                {"name": "name"}
            ]
        }
    ]


def test_load_simple_object_with_params():
    assert graphql.loads("""
    {
        user(232) {
            id,
            name
        }
    }""") == [
        {
            "name": "user",
            "params": 232,
            "properties": [
                {"name": "id"},
                {"name": "name"}
            ]
        }
    ]


def test_load_simple_object_with_filters():
    assert graphql.loads("""
    {
        photos.first(2) {
            url,
            width,
            height
        }
    }""") == [
        {
            "name": "photos",
            "filters": {"first": 2},
            "properties": [
                {"name": "url"},
                {"name": "width"},
                {"name": "height"},
            ]
        }
    ]


def test_load_simple_object_with_full_header():
    assert graphql.loads("""
    {
        photos(username: "Louro Jose").after(id: 232).sortBy("username") {
            url,
            width,
            height
        }
    }""") == [
        {
            "name": "photos",
            "params": {"username": "Louro Jose"},
            "filters": {
                "after": {"id": 232},
                "sortBy": "username"
            },
            "properties": [
                {"name": "url"},
                {"name": "width"},
                {"name": "height"},
            ]
        }
    ]


def test_load_simple_object_with_full_header_multiple_args():
    assert graphql.loads("""
    {
        photos(username: "Louro Jose").after(id: 232, username: "Hebe").sortBy("url") {
            url,
            width,
            height
        }
    }""") == [
        {
            "name": "photos",
            "params": {"username": "Louro Jose"},
            "filters": {
                "after": {"id": 232, "username": "Hebe"},
                "sortBy": "url"
            },
            "properties": [
                {"name": "url"},
                {"name": "width"},
                {"name": "height"},
            ]
        }
    ]


def test_load_multiple_objects():
    assert graphql.loads("""
    {
        user(232) {
            name,
            id
        },
        company(userId: 232) {
            address
        }
    }""") == [
        {
            "name": "user",
            "params": 232,
            "properties": [
                {"name": "name"},
                {"name": "id"}
            ]
        },
        {
            "name": "company",
            "params": {"userId": 232},
            "properties": [
                {"name": "address"}
            ]
        }
    ]


def test_load_objects_with_constant_args():
    assert graphql.loads('{ user(null) { id } }') == [
        {
            "name": "user",
            "params": None,
            "properties": [ {"name": "id"} ]
        }
    ]

    assert graphql.loads('{ user(true) { id } }') == [
        {
            "name": "user",
            "params": True,
            "properties": [ {"name": "id"} ]
        }
    ]

    assert graphql.loads('{ user(false) { id } }') == [
        {
            "name": "user",
            "params": False,
            "properties": [ {"name": "id"} ]
        }
    ]

    assert graphql.loads('{ user(id: null) { id } }') == [
        {
            "name": "user",
            "params": {"id": None},
            "properties": [ {"name": "id"} ]
        }
    ]

def test_nested_objects():
    assert graphql.loads("""
    {
        user(232) {
            id,
            name,
            photo(size: 50) {
                url,
                width,
                height
            }
        }
    }
    """) == [
        {
            "name": "user",
            "params": 232,
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
    ]

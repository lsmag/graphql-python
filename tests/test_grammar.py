# -*- coding: utf-8 -*-
from contextlib import contextmanager
from pyparsing import ParseException
from graphql import grammar


@contextmanager
def assert_raises(exc):
    raised = True
    try:
        yield
        raised = False
    except Exception as e:
        assert isinstance(e, exc)

    assert raised, "Exception %s not raised" % exc


def test_literals():
    assert grammar.literal.parseString('null').asList() == ['null']
    assert grammar.literal.parseString('true').asList() == ['true']
    assert grammar.literal.parseString('false').asList() == ['false']

    assert grammar.literal.parseString('2.334').asList() == ['2.334']
    assert grammar.literal.parseString('-12.334').asList() == ['-12.334']
    assert grammar.literal.parseString('42').asList() == ['42']

    assert grammar.literal.parseString('"Foobar"').asList() == ['"Foobar"']
    assert grammar.literal.parseString("'Barbaz'").asList() == ["'Barbaz'"]


def test_identifier():
    assert grammar.identifier.parseString('fooBar').asList() == ['fooBar']
    assert grammar.identifier.parseString('foo23_45').asList() == ['foo23_45']
    assert grammar.identifier.parseString('entity/23').asList() == ['entity/23']
    assert grammar.identifier.parseString('_foo').asList() == ['_foo']

    with assert_raises(ParseException):
        grammar.identifier.parseString('/fas').asList()

    with assert_raises(ParseException):
        grammar.identifier.parseString('42as').asList()


def test_params_list():
    # Testing literals
    assert grammar.params_list.parseString('(null)').asList() == ['null']
    assert grammar.params_list.parseString('(true)').asList() == ['true']
    assert grammar.params_list.parseString('(false)').asList() == ['false']
    assert grammar.params_list.parseString('(2333.43)').asList() == ['2333.43']
    assert grammar.params_list.parseString('("foo")').asList() == ['"foo"']

    # Pairs
    assert grammar.params_list.parseString('(id: 12, name: "Adalberto")').asList() == [['id', '12'], ['name', '"Adalberto"']]
    assert grammar.params_list.parseString('(component/name: "textarea")').asList() == [['component/name', '"textarea"']]

    # Empty params list
    assert grammar.params_list.parseString('()').asList() == []


def test_gql_header():
    # Valid headers:
    # user {
    # user(232) {
    # user(id: 232) {
    # photos.first(2) {
    # friends(recent: true).first(50) {
    assert grammar.gql_header.parseString('user').asList() == ['user', []]
    assert grammar.gql_header.parseString('user(232)').asList() == ['user', ['232'], []]
    assert grammar.gql_header.parseString('user(id: 232, name: "Adalberto")').asList() == ['user', [['id', '232'], ['name', '"Adalberto"']], [] ]

    assert grammar.gql_header.parseString('photos.first(2)').asList() == ['photos', [ ['first', '2'] ]]

    assert grammar.gql_header.parseString('friends.after(2434423).first(10)').asList() == ['friends', [ ['after', '2434423'], ['first', '10'] ]]

    assert grammar.gql_header.parseString('friends(recent: true).first(50)').asList() == ['friends', [['recent', 'true']], [['first', '50']] ]

    # We need to test if groups are labeled properly
    res = grammar.gql_header.parseString('friends(id: 42, recent: true).first(50)')
    assert res['params'].asList() == [['id', '42'], ['recent', 'true']]
    assert res['filters'].asList() == [['first', '50']]

    res = grammar.gql_header.parseString('user')
    assert 'params' not in res
    assert ('filters' not in res or not res['filters'])


def test_gql_object():
    assert grammar.gql_object.parseString("""
        user {
            id,
            name
        }
    """).asList() == [['user', []], ['id', 'name']]

    with assert_raises(ParseException):
        grammar.gql_object.parseString('user {}')

    obj = """
        user(232) {
            id,
            name
        }
    """
    assert grammar.gql_object.parseString(obj).asList() == [['user', ['232'], []], ['id', 'name']]
    assert grammar.gql_object.parseString(obj)['header'].asList() == ['user', ['232'], []]
    assert grammar.gql_object.parseString(obj)['properties'].asList() == ['id', 'name']

    assert grammar.gql_object.parseString("""
        user(232) {
            id,
            name,
            photo(size: 50) {
                url,
                id
            }
        }
    """).asList() == (
        [
            ['user', ['232'], []],
            ['id',
             'name',
             [
                 ['photo', [['size', '50']], []],
                 ['url', 'id']
             ]
            ]
        ]
    )


def test_root():
    # root is the main grammar, it defines a list of objects
    assert grammar.root.parseString("""
    {
        User(f: "123", g: 223) {
            id,
            name
        },

        AnotherUser {
            id,
            name
        }
    }
    """).asList() == [
        [
            ['User', [['f', '"123"'], ['g', '223']], []],
            ['id', 'name']
        ],
        [
            ['AnotherUser', []],
            ['id', 'name']
        ]
    ]

    # Missing commas between objects will raise an exception
    with assert_raises(ParseException):
        grammar.root.parseString("""
        {
            User {id, name}
            AnotherUser {id, name}
        }""")

    # Anything after the end of the document will raise an exception
    with assert_raises(ParseException):
        grammar.root.parseString("""
        {
            User {id, name},
            AnotherUser {id, name}
        } foo bar""")

    # Likewise, anything before also will raise an exception
    with assert_raises(ParseException):
        grammar.root.parseString("""
        foo bar{
            User {id, name},
            AnotherUser {id, name}
        }""")

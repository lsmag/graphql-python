GraphQL parser for Python
=========================

This is an experimental, generic parser for the [GraphQL language][1] in Python. Consider it unstable since there's no spec for the language yey (that's why it's *experimental* ;)


Install and usage
-----------------

    $ pip install graphql-python

And just `import graphql` to get started. This library mimics the standard `json` module, so there's a `dumps` and a `loads` function. Consider this query:

    query = """
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
    """

    objects = graphql.loads(query)
    # objects has now:
    [
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
		            },
            ]
	      }
    ]

To understand how `loads` works, let's split this query into small parts:

    friends(user_id: 232).first(10) {
        url,
        name,
        address
    }

This query represents an *object* composed of:

 - a name (`friends`)
   - can be anything that matches the `r'`[a-zA-Z_][a-zA-Z0-9_/]*'` regex.
 - some parameters (`user_id: 232`)
   - can match literals (strings, numbers with or without signal, true, false and null) and pairs of values
   - `(true)` will be loaded as `"params": True`. Likewise, `(232)` will be `"params": 232`.
   - `(foo: "bar", bar: "baz")` will be loaded as `"params": {"foo": "bar", "bar": "baz"}`. Any valid identifier (the regex for *name*) can be used as an argument.
 - some custom filters (`first(10)`)
   - it's a sequence of identifiers followed by a list of parameters. Order is important, so for example, `.after(id: 243442).first(10)` will be loaded as:


        "filters": [
            ("after", {"id": 243442}),
	        ("first", 10)
        ]
	

 - and a list of properties (`url, name, address`)... basically either an identifier or another nested object.


Some advices
------------

Right now, this parser is *strict* (at least until the spec is released, obviously). It'll yell at you for not using commas in the right places. For example:

    # Will fail :(
    graphql.loads("""
        user(42) {
            id,
            name
      	}
    """)

    # Much better :) ... don't forget those { } in the beginning and end of the query 
    graphql.loads("""
    {
        user(42) {
	        id,
            name
      	}
    }
    """)

    # Will fail :(
    graphql.loads("""
    {
        user(42) {
            id,
            name
      	}

        company(2) {
            address
      	}
    }
    """)

    # Much better :) ... see that little comma right after the first object?
    graphql.loads("""
    {
        user(42) {
      	    id,
      	    name
      	},  # <-- right here

        company(2) {
      	    address
      	}
    }
    """)


A note about performance & pyParsing
------------------------------------

I didn't test the numbers, just dropping [this link][2] for you to tell there's a way to improve pyParsing's performance.
This flag isn't enabled because it's global, so [YMMV][3].

[1]: https://facebook.github.io/react/blog/2015/05/01/graphql-introduction.html
[2]: http://stackoverflow.com/a/21371472
[3]: http://www.urbandictionary.com/define.php?term=ymmv

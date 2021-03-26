# Main Components

These are the parts of the library that you'll probably have to use, no matter how you decide to do things.

## Routing

Routing is the way of linking a location to some resource.

Whilst routes may appear to be dynamic in nature, they are also `exhaustive`. That is, they aren't actually infinitely capable, because we are still generated a flat series of files. There is no JS fuckery under the hood that will make history explode when something goes wrong - unless you put it there.

Routes take a similar form to a Python format string, for example:

	/users/{username:users}

This similarity isn't by accident. The string will be parsed using Python's format string parser, which means you'll need to follow the same rules as it.

The only difference is that the `type specifier` referse to one of our truth sources (supplied to either `staticweb.source` or `staticweb.compile`).

The function you attach to a route _must_ accept the arguments specified in the route.

As routes are `exhaustive`, the more components you add to a route, the more you'll increase your rendering times. However, the `logging` facilities should help you track down where the most time is spent, rather than making an assumption.

For more information, see `Decorators/staticweb.route` or `API/staticweb.route`.

## Sources

Sources are where you can specify the exhaustive list of possible results that get bound into routes.

These functions can come from anywhere, and there are just two caveats:

+ They must supply a list of string-formattable data that can fit inside a valid URL.

+ They must be exhaustive - that is, they must terminate. You can't have an infinite loop or anything like that without breaking your build process.

An example source might be:

	import sqlite3

	def user():
		db = sqlite3.connect("my.db")
		users = []

		for row in db.execute("SELECT username FROM users"):
			users.append(row[0])
		db.close()

		return users

And then you expose it by supplying a key/value pair:

	staticweb.source(user=user)

The `type specifier` in a route will match against the given key.

Sources can be supplied anywhere before the `compilation` stage.

For more information, see `API/staticweb.source`.

## Compiling

Once all routes, functions and sources are created and you're happy, then it is time to compile!

This will attempt to generate the entire site to a directory.

The simplest version of doing this is:

	staticweb.compile()

For more information see `API/staticweb.compile`.

If you're hitting errors during compilation, it can be helpful to get more logging information. You can do that by adjust Python's logger in the usual way.

Put something like this at the top of your file:

	import logging
	logging.basicConfig(level=logging.DEBUG)

## Logging

The library `staticweb` uses Python's normal logging facilities.

At its most basic, put something like this at the top of your file:

	import logging
	logging.basicConfig(level=logging.DEBUG)

To get more logging information.

Expect to get a _lot_ of information at that level.

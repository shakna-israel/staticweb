# HTML Generation

The library `staticweb` comes with a few helpers for live-generating HTML data in a somewhat DOM-like manner.

## staticweb.HTMLResponse

The main parts of a HTMLResponse are:

+ The `lang` attribute, which would usually be either `None` or something like `"en"`.

+ The `doctype` attribute, which would usually be something like `"utf8"`.

+ The `head` attribute, which is a `staticweb.HTMLElement`, but with a few... Quirks. Because HTML is quirky.

+ The `body` attribute, which is a `staticweb.HTMLElement`.

+ A bunch of helper methods.

The basic usage should make things a little clearer:

	r = staticweb.HTMLResponse(title="Home")

	content = staticweb.HTMLElement("div")

	text = staticweb.HTMLElement("p")
	text.addText("Hello, World!")
	content.appendChild(text)

	r.body.appendChild(content)

	return r

It should feel _somewhat_ like DOM manipulation in JS.

## staticweb.HTMLElement

This is what compiles down to a HTML string.

The main components are:

+ A `dict` connected to the `data` attribute, for storing `dataset` values.

+ You can add arbitrary attributes, and expect them to appear as HTML element attributes.

+ You can append/prepend arbitrary elements using `appendChild` and `prependChild`.

If you use `"plain/text"` as a constructor, you'll get straight text that isn't an element, but can be manipulated in a similar manner, to make things easier.

# API

## `staticweb.source(**kwargs) -> None`

This function takes a series of key/value pairs.

Keys will be used as `type specifiers` in routes.

Values should be functions as expected by the router.

See `Decorators/staticweb.route` or `API/staticweb.route` for more.

## `staticweb.sendfile(path) -> pathlib.Path`

This turns a path into an appropriate `Path` object that will only be read at compile time.

This is just a convenience function.

See `API/staticweb.compile` for more.

## `class staticweb.HTMLResponse(charset="utf8", doctype="html", title=None, lang=None)`

This constructs a base `HTMLResponse` object.

All the attributes from creation can later be modified.

This is the class you would use when generating a HTML file from scratch, where you might more traditionally use a HTML generator.

This is just for convenience - you can still import and use whatever HTML generator you are most comfortable with.

### `staticweb.HTMLResponse.head -> staticweb.HTMLElement`

This attribute of an existing `HTMLResponse` object refers to the `head` element.

When modified using other methods, some quirks of HTML are attempted to be taken into account.

More manual intervention requires that you manually call `staticweb.HTMLResponse.verify`.

### `staticweb.HTMLResponse.body -> staticweb.HTMLElement`

This attribute of an existing `HTMLResponse` object refers to the `body` element.

### `staticweb.HTMLResponse.verify(self) -> self`

This function will attempt to repair a response to fit the quirks that exist within the HTML specification.

### `staticweb.HTMLResponse.set_title(self, title_content) -> self`

This function will set the `title` element inside the HTML `head` element.

This is a convenience function.

### `staticweb.HTMLResponse.set_charset(self, new_charset) -> self`

This function will attempt to set the `charset` via a `meta` element inside the HTML `head`.

This is a convenience function.

### `staticweb.HTMLResponse.set_lang(self, new_lang) -> self`

This function will set the `lang` attribute to appear on the `html` element.

### `staticweb.HTMLResponse.http_header(self, header, content) -> self`

This is a convenience function for adding a `meta http-equiv` element to the HTML `head` element.

### `staticweb.HTMLResponse.as_dict(self) -> dict`

This function returns a structured `dict` that can be freely modified representing the state of the given `HTMLResponse`.

The data generated should be able to be serialised to JSON with Python's typical `dict->json` tools.

### `staticweb.HTMLResponse.from_dict(self, data) -> self`

This function takes a structured `dict`, like the one created from `staticweb.HTMLResponse.as_dict`, and applies it to the current `HTMLResponse` object. Allowing you to deserialise the object.

### `staticweb.HTMLResponse.compile(self) -> str`

This will attempt to take the given `HTMLResponse` object and turn it into a flat string. This can be saved to a file, printed, etc.

### `staticweb.HTMLResponse.__repr__(self) -> str`

This calls `staticweb.HTMLResponse.compile`, allowing you to `print(HTMLResponse)` or whatever else you'd like to do.

## `class staticweb.HTMLElement(element: str)`

This constructs a base `HTMLElement` object.

The given `element` should be a valid HTML tag name or `"plain/text"`.

The `"plain/text"` element is used to represent plain text, unenclosed by an element.

### `staticweb.HTMLElement.data`

This attribute of a base `HTMLElement` object is a dictionary, that will compile down to [dataset](https://developer.mozilla.org/en-US/docs/Web/API/HTMLOrForeignElement/dataset) attributes, and most of the caveats about key-naming from the spec follows.

The values will be formatted, or attempted to be formatted, to fit as best the system can handle, but expect it to be a string in the end.

### `staticweb.HTMLElement.__dict__`

Any attributes added to a base `HTMLElement` object by the programmer will be attempted to be converted to HTML attributes upon compilation.

A handful of attributes are reserved, and can be found under `HTMLElement.default_attributes`.

There is no verification if an attribute makes sense and is allowed by the HTML spec - it is up to the programmer to do what makes sense.

In the case of a `"plain/text"` element, you can also supply the `textContent` attribute to control its contents. (This usually would be treated like a normal attribute).

### `staticweb.HTMLElement.appendChild(self, childElement: staticweb.HTMLElement) -> self`

Appends a given element as the last child of the original `HTMLElement` object.

If the element is in the list of HTML void elements (self-closing), it may raise a `RuntimeError`.

### `staticweb.HTMLElement.prependChild(self, childElement: staticweb.HTMLElement) -> self`

Works the same as `staticweb.HTMLElement.appendChild`, but it prepends to the list of children, instead of appending.

### `staticweb.HTMLElement.addText(self, some_text: str) -> self`

This creates a `"plain/text"` element, containing the given string, and appends it to the list of children.

This is a convenience method.

### `staticweb.HTMLElement.as_dict(self) -> dict`

This converts the given object into a `dict` representation.

### `staticweb.HTMLElement.from_dict(self, data) -> self`

Given a structured `dict`, like produced by `staticweb.HTMLElement.as_dict`, it will convert the current `HTMLElement` to match.

## `staticweb.HTMLView`

This is a decorator that will take a `dict` returned by a function route and attempt to generate a `HTMLResponse` from it, as given by something like `staticweb.HTMLResponse.from_dict`.

See also `Decorators/staticweb.HTMLView` and `API/staticweb.HTMLResponse.from_dict`.

## `staticweb.redirect(path, timeout=0, message="Redirecting...") -> staticweb.HTMLResponse`

This will create a `staticweb.HTMLResponse` containing a `http-equiv` `Refresh` method for the given `path`.

This is a convenience method.

## `staticweb.route(path: str)`

This decorator links a given `path` to a `function`, and will be used to generate one or more files for the static site.

The string given as a `path` should match Python's format specification, but where the `type specifier` matches a given `source`.

For example:

	@staticweb.route("/gen/{username:get_user}")
	def gen(username):
		return "Hello, {}".format(username)

If the `path` does not end with a file extension, then the generated file will be found at `{path}/index.html`.

Paths are parsed, using the given source functions to get all possible matches, and every possible combination will be created from that.

_All_ dynamic parts of the URL will be passed to the underlying function, which should expect to receive them.

See also `API/staticweb.source`, `Decorators/staticweb.route`, `Main Components/Routing`.

## `staticweb.compile(build_dir="_build", sources=None) -> None`

Optionally takes a dict as sources, which is sent to `staticweb.source`.

This will attempt to create the given site under the given `build_dir` path. It won't attempt to clean or destroy any existing files that are not overwritten by the generated site.

This should be called as one of the last parts of your program.

## `staticweb.run(build_dir="_build", PORT=8080) -> None`

This function doesn't call `staticweb.compile`, you'll need to do that on your own.

All this does is spawn a simple and pathetic static file server using the given `build_dir` path on the given `PORT`.

This is a convenience function.

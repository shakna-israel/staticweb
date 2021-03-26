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

The given `element` should be a valid HTML tag name.

### `staticweb.HTMLElement.data`

TODO

### `staticweb.HTMLElement.__dict__`

TODO

### `staticweb.HTMLElement.appendChild(self, childElement: staticweb.HTMLElement) -> self`

TODO

### `staticweb.HTMLElement.prependChild(self, childElement: staticweb.HTMLElement) -> self`

TODO

### `staticweb.HTMLElement.addText(self, some_text: str) -> self`

TODO

### `staticweb.HTMLElement.as_dict(self) -> dict`

TODO

### `staticweb.HTMLElement.from_dict(self, data) -> self`

TODO

## `staticweb.HTMLView`

TODO

## `staticweb.redirect(path, timeout=0, message="Redirecting...") -> staticweb.HTMLResponse`

TODO

## `staticweb.route(path)`

TODO

## `staticweb.compile(build_dir="_build", sources=None) -> None`

TODO

## `staticweb.run(build_dir="_build", PORT=8080) -> None`

TODO

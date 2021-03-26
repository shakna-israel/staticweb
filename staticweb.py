"""
staticweb.py

Copyright 2021, James Milne

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import string
import itertools
import pathlib
import json
import html
import logging

routes = {}
sources = {}

def source(**kwargs):
	# Add the sources we'll gather data from...
	for k, v in kwargs.items():

		logging.debug("Adding source: {}".format(k))

		sources[k] = v

def sendfile(path):
	logging.debug("Lazy-linking static file: <{}>".format(path))
	return pathlib.Path(path)

class PathTemplate(string.Formatter):
	def __init__(self, *args, **kwargs):
		super(PathTemplate, self)

		self.values = {}

	def parse(self, format_string):
		t = super(PathTemplate, self).parse(format_string)
		t = list(t)

		for cell in t:
			literal_text, field_name, format_spec, conversion = cell

			if format_spec != None:
				self.values[field_name] = sources[format_spec]()

		return t

	def format_field(self, value, spec):
		# Custom behaviour: Ignores the spec formatter
		return super(PathTemplate, self).format_field(value, "")

	def matches(self, path):
		# Footgun: Assumes that self.parse has already been called.

		r = []

		if len(self.values) > 0:
			keys, values = zip(*self.values.items())
			permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]

			for item in permutations_dicts:

				datum = {}
				datum['path'] = self.format(path, **item)
				datum['args'] = item
				r.append(datum)

		else:
			datum = {}
			datum['path'] = self.format(path)
			datum['args'] = {}
			r = [datum]

		logging.debug("Generated matches: {}".format(r))

		return r

class HTMLResponse(object):
	def __init__(self, charset="utf8", doctype="html", title=None, lang=None):
		self.doctype = doctype
		self.head = HTMLElement("head")
		self.body = HTMLElement("body")

		# Sensible default elements!

		# charset
		charset_el = HTMLElement("meta")
		charset_el.charset = charset
		self.head.appendChild(charset_el)

		# viewport
		viewport = HTMLElement("meta")
		viewport.name = "viewport"
		viewport.content = "width=device-width, initial-scale=1"
		self.head.appendChild(viewport)

		# title
		if title != None:
			title_el = HTMLElement("title")
			title_text = HTMLElement("plain/text")
			title_text.textContent = title
			title_el.appendChild(title_text)
			self.head.appendChild(title_el)

		self.lang = lang

		logging.debug("New HTMLResponse: {}".format(self.as_dict()))

	def __repr__(self):
		return self.compile()

	def verify(self):
		logging.debug("Verifying HTMLResponse")

		# Handle hoisting and other quirks

		# Remove absolute duplicates from head
		tmp_head = self.head.as_dict()
		children = tmp_head['children']

		set_of_jsons = {json.dumps(d, sort_keys=True) for d in children}
		X = [json.loads(t) for t in set_of_jsons]
		tmp_head['children'] = X
		self.head.from_dict(tmp_head)

		# Only one title element! (Doesn't break if title is a child of noscript!)
		title = [idx for idx, element in enumerate(self.head.children) if element.element == 'title']
		if title:
			# Get the last title set...
			title = self.head.children.pop(title[-1])

			new_head = []
			for element in self.head.children:
				if not (element.element == 'title'):
					new_head.append(element)
			self.head.children = new_head
			self.head.prependChild(title)

		# Hoisting must happen _last_!

		# <meta name="viewport"> _must_ be second-to-top element!
		viewport = [idx for idx, element in enumerate(self.head.children) if element.element == "meta" and hasattr(element, "name") and element.name == 'viewport']
		if viewport:
			# Get the last viewport set...
			viewport = self.head.children.pop(viewport[-1])

			# Ensure only one viewport element
			new_head = []
			for element in self.head.children:
				if not (element.element == 'meta' and hasattr(element, "name") and element.name == 'viewport'):
					new_head.append(element)
			self.head.children = new_head


			# Prepend the viewport
			self.head.prependChild(viewport)

		# <meta charset="utf-8"> _must_ be first element!
		charset = [idx for idx, element in enumerate(self.head.children) if element.element == 'meta' and hasattr(element, "charset")]
		if charset:
			# Get the last charset set...
			charset = self.head.children.pop(charset[-1])

			# Ensure only one charset element
			new_head = []
			for element in self.head.children:
				if not (element.element == 'meta' and hasattr(element, "charset")):
					new_head.append(element)
			self.head.children = new_head
			
			# Prepend the charset
			self.head.prependChild(charset)

		return self

	def set_title(self, title_content):
		logging.debug("Changing HTMLResponse title via convenience helper: <{}>".format(title_content))

		title_el = HTMLElement("title")
		title_text = HTMLElement("plain/text")
		title_text.textContent = title_content
		title_el.appendChild(title_text)
		self.head.appendChild(title_el)

		# Handle quirks!
		self.verify()

		# Allow chaining
		return self

	def set_charset(self, new_charset):
		logging.debug("Changing HTMLResponse charset via convenience helper: <{}>".format(new_charset))

		charset_el = HTMLElement("meta")
		charset_el.charset = new_charset
		self.head.appendChild(charset_el)

		# Handle quirks!
		self.verify()

		# Allow chaining
		return self

	def set_lang(self, new_lang):
		logging.debug("Changing HTMLResponse lang via convenience helper: <{}>".format(new_lang))

		self.lang = new_lang

		# Allow chaining
		return self

	# TODO: A set_cookie helper compatible with JS

	def http_header(self, header, content):
		logging.debug("Create a http-equiv element via convenience helper: <{}> <{}>".format(header, content))

		tmp = HTMLElement("meta")
		setattr(tmp, "http-equiv", header)
		setattr(tmp, "content", content)
		self.head.appendChild(tmp)

		# Handle quirks!
		self.verify()

		# Allow chainging
		return self

	def as_dict(self):
		logging.debug("Creating dict from HTMLResponse")

		# Handle quirks!
		self.verify()

		return {"doctype": self.doctype,
			"lang": self.lang,
			"head": self.head.as_dict(),
			"body": self.body.as_dict()}

	def from_dict(self, data):
		logging.debug("Creating HTMLResponse from dict: <{}>".format(data))

		self.doctype = data['doctype']

		try:
			self.lang = data['lang']
		except:
			self.lang = None

		self.head.from_dict(data['head'])
		self.body.from_dict(data['body'])

		# Handle quirks!
		self.verify()

		return self

	def compile(self):
		logging.debug("Rendering HTMLResponse")

		# Handle quirks!
		self.verify()

		if self.lang:
			return """<!DOCTYPE {doctype}>
<html lang={lang}>
{head}
{body}""".format(doctype=self.doctype,
			head=self.head,
			body=self.body,
			lang=self.lang)
		else:
			return """<!DOCTYPE {doctype}>
{head}
{body}""".format(doctype=self.doctype,
			head=self.head,
			body=self.body)

class HTMLElement(object):
	def __init__(self, element):
		self.element = element
		self.data = {}

		self.void_elements = ['area',
			'base',
			'br',
			'col',
			'embed',
			'hr',
			'img',
			'input',
			'link',
			'meta',
			'param',
			'source',
			'track',
			'wbr',
			'command',
			'keygen',
			'menuitem'
		]

		self.children = []

		self.default_attributes = ['element', 'data', 'void_elements', 'children', 'default_attributes']

	def __repr__(self):
		logging.debug("Rendering HTMLElement")

		# Special handling for just text elements...
		if self.element == 'plain/text':
			if getattr(self, "textContent"):
				return self.textContent
			else:
				return ''

		# Assemble dataset values
		dataset_values = []
		for key, value in self.data.items():
			# Convert name accord to spec...
			spec_allowed = string.ascii_lowercase + string.digits + '-.:_'
			key = ''.join([letter for letter in key.lower() if letter in spec_allowed])
			key = "data-{}".format(key)

			# Escape the value so we can replace quotes properly...
			value = html.escape(value)
			
			# TODO: Is this needed...? Maybe... Sometimes, but not always??
			# Escape invalid stuff like newlines
			value = value.encode('unicode_escape').decode()

			dataset_string = "{key}=\"{value}\"".format(key=key, value=value)

			dataset_values.append(dataset_string)

		dataset_string = ' '.join(dataset_values).strip()
		if dataset_string:
			dataset_string = " {}".format(dataset_string)

		# Assemble attributes string.
		attributes = [x for x in self.__dict__ if x not in self.default_attributes]
		attr_string = ""
		for attribute in attributes:

			# Get the value from the dict...
			value = self.__dict__[attribute]
			# Escape it so we can replace quotes properly...
			value = html.escape(value)
			
			# TODO: Is this needed...? Maybe... Sometimes, but not always??
			# Escape invalid stuff like newlines
			value = value.encode('unicode_escape').decode()

			attr_string="{} {attribute}=\"{value}\"".format(attr_string,
				attribute=attribute,
				value=value)

		attr_string = attr_string.strip()
		if attr_string:
			attr_string = " {}".format(attr_string)

		# Assemble final element...
		if self.element in self.void_elements:
			# Children aren't possible for a self-closing (void) element:
			return "<{element}{attr}{data} />".format(element=self.element, attr=attr_string, data=dataset_string)
		else:
			# Render any children...
			kids = ''.join(str(child) for child in self.children)
			return "<{element}{attr}{data}>{kids}</{element}>".format(element=self.element, kids=kids, attr=attr_string, data=dataset_string)

	def appendChild(self, childElement):
		logging.debug("Appending HTML Child Element")

		if self.element in self.void_elements:
			raise RuntimeError("<{}> cannot have children as it is a HTML5 void element.".format(self.element))
		else:
			self.children.append(childElement)

		# Return self to enable chaining...
		return self

	def prependChild(self, childElement):
		logging.debug("Prepending HTML Child Element")

		if self.element in self.void_elements:
			raise RuntimeError("<{}> cannot have children as it is a HTML5 void element.".format(self.element))
		else:
			self.children.insert(0, childElement)

		# Return self to enable chaining...
		return self

	def addText(self, some_text):
		logging.debug("Appending plain/text HTMLElement via convenience helper.")

		tmp = HTMLElement("plain/text")
		tmp.textContent = some_text
		self.appendChild(tmp)

		# Allow chaining
		return self

	def as_dict(self):
		logging.debug("Creating dict from HTMLElement")

		payload = {"element": self.element, "data": self.data}

		attr_dict = {}

		attributes = [x for x in self.__dict__ if x not in self.default_attributes]
		for attribute in attributes:
			attr_dict[attribute] = self.__dict__[attribute]

		payload['attributes'] = attr_dict
		payload['children'] = [child.as_dict() for child in self.children]
		return payload

	def from_dict(self, data):
		logging.debug("Creating HTMLElement from dict")

		# Set the kind
		self.element = data['element']

		# Remove all existing attributes
		attributes = [x for x in self.__dict__ if x not in self.default_attributes]
		for attribute in attributes:
			del self.__dict__[attribute]

		# Recreate the attributes
		for attr, val in data['attributes'].items():
			setattr(self, attr, val)

		# Remove all dataset
		self.data = {}

		# Recreate the data
		for k, v in data['data'].items():
			self.data[k] = v

		# Remove all children
		self.children = []

		# Recreate the children
		for child in data['children']:
			tmp = HTMLElement(child['element'])
			tmp.from_dict(child)
			self.appendChild(tmp)

		# Allow chaining...
		return self

def HTMLView():
	logging.debug("Creating HTMLView")

	def html_view(func):
		def html_compiled_view(*args, **kwargs):
			data_dict = func(*args, **kwargs)
			r = HTMLResponse()
			r.from_dict(data_dict)
			return r
		return html_compiled_view

	return html_view

def redirect(path, timeout=0, message="Redirecting..."):
	logging.debug("Creating HTML-based redirect")

	r = HTMLResponse(title="Redirecting...")

	text = HTMLElement("p")
	text.addText(message)

	r.body.appendChild(text)
	r.http_header("refresh", "{}; {}".format(timeout, path))

	return r

def route(path):
	logging.debug("Generating route")

	def route_link(func):
		routes[path] = func
	return route_link

def compile(build_dir="_build", sources=None):
	# Allow passing sources dict to compile
	if sources != None:
		source(**sources)

	if not isinstance(build_dir, pathlib.Path):
		build_dir = pathlib.Path(build_dir)

	if not build_dir.exists():
		logging.warning("Created build directory: <{}>".format(build_dir))
		build_dir.mkdir()
	else:
		logging.warning("Build directory already exists (may contain stale data): <{}>".format(build_dir))

	# Iterate all given routes
	for path, func in routes.items():

		# Prepare to get exhaustive matches
		parser = PathTemplate()
		parser.parse(path)

		# Get an exhaustive list of matches
		all_matches = parser.matches(path)

		for match in all_matches:
			logging.debug("Processing route: <{}>".format(match))

			# Execute the equivalent function with all the right arguments
			result = func(**match['args'])

			# Build the path
			if not (build_dir / match['path']).suffix:
				# No suffix, probably meant to be a html file
				outpath = build_dir / match['path'] / 'index.html'
			else:
				# Has a file suffix, don't guess
				outpath = build_dir / match['path']

			if str(outpath)[0] == '/':
				outpath = pathlib.Path(str(outpath)[1:])
				outpath = build_dir / outpath

			# Ensure the directory exists
			if not outpath.parent.exists():
				logging.warning("Creating all directories for: <{}>".format(outpath.parent))
				outpath.parent.mkdir(parents=True)

			# Re/create the file!
			with open(outpath, "wb+") as openFile:
				# Our HTML Builder...
				if isinstance(result, HTMLResponse):
					logging.info("Creating a HTML file.")

					r = result.compile()
					openFile.write(r.encode())
				# JSON serialiser...
				elif isinstance(result, dict) or isinstance(result, list):
					logging.info("Creating a JSON file.")

					openFile.write(json.dumps(result).encode())
				# pathlib/sendfile serialiser...
				elif isinstance(result, pathlib.Path):
					logging.info("Creating a file from the linked: <{}>".format(result))

					with open(result, 'rb') as fp:
						openFile.write(fp.read())
				# Everything else...
				else:
					logging.info("Creating raw file")

					openFile.write(result.encode())

def run(build_dir="_build", PORT=8080):
	import http.server
	import socketserver

	class Handler(http.server.SimpleHTTPRequestHandler):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, directory=build_dir, **kwargs)

	with socketserver.TCPServer(("", PORT), Handler) as httpd:
		logging.warning("THIS SERVER SHOULD NEVER BE USED IN PRODUCTION")
		logging.info("Server started at http://0.0.0.0:" + str(PORT))

		try:
			httpd.serve_forever()
		except:
			httpd.server_close()

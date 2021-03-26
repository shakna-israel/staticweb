# staticweb.py

A Pythonic framework for your static site.

---

# About

This is a 0-dependency library for creating static websites whilst making the programmer feel like they're using a pretty standard Python WSGI framework.

---

# A Taste

	import staticweb

	# Create some sources...
	def get_user():
		return ['jmilne', 'phil']

	def foo():
		return ['foo', 'bar', 'baz']

	# Let the generator know the sources of truth...
	staticweb.source(get_user=get_user, foo=foo)

	@staticweb.route("/")
	def index():
		# A route using our HTMLResponse helper

		r = staticweb.HTMLResponse(title="Home")

		content = staticweb.HTMLElement("div")

		text = staticweb.HTMLElement("p")
		text.addText("Hello, World!")
		content.appendChild(text)

		r.body.appendChild(content)

		return r

	@staticweb.route("/{username:get_user}/{this:foo}")
	def user_public(username, this):
		# A route that uses our sources of truth...

		return "Hello, {}".format(username)

	@staticweb.route("/file.json")
	def datafile():
		# A route that creates a JSON file...

		return {"hello": "world"}

	@staticweb.route("/staticfile.py")
	def statfile():
		# A route that copies a static file...

		return staticweb.sendfile("demo.py")

	@staticweb.route("/something")
	def moved():
		# A route that redirects...

		return staticweb.redirect("/file.json")

	if __name__ == "__main__":
		staticweb.compile()

		# Start a basic HTTP Server for dev testing...
		staticweb.run()

---

# Documentation

See the `docs` folder.

---

# License

See the head of the `staticweb.py` file for legally binding text.

3-Clause BSD at time of writing.

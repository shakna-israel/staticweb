import staticweb

#import logging
#logging.basicConfig(level=logging.DEBUG)

def get_user():
	# Spec formatter to return exhaustive list of users
	return ['jmilne', 'phil']

def that():
	# Spec formatter returns exhaustive list, always
	return ['that']

@staticweb.route("/")
def index():
	r = staticweb.HTMLResponse(title="Home")

	content = staticweb.HTMLElement("div")

	text = staticweb.HTMLElement("p")
	text.addText("Hello, World!")
	content.appendChild(text)

	r.body.appendChild(content)

	r.set_cookie("session", "hello")

	return r

@staticweb.route("/gen/{username:get_user}")
@staticweb.HTMLView()
def gen_view(username):
	return {'doctype': 'html', 'head': {'element': 'head', 'data': {}, 'attributes': {}, 'children': [{'element': 'meta', 'data': {}, 'attributes': {'charset': 'utf8'}, 'children': []}, {'element': 'meta', 'data': {}, 'attributes': {'content': 'width=device-width, initial-scale=1', 'name': 'viewport'}, 'children': []}, {'element': 'title', 'data': {}, 'attributes': {}, 'children': [{'element': 'plain/text', 'data': {}, 'attributes': {'textContent': 'Home'}, 'children': []}]}]}, 'body': {'element': 'body', 'data': {}, 'attributes': {}, 'children': [{'element': 'div', 'data': {}, 'attributes': {}, 'children': [{'element': 'p', 'data': {}, 'attributes': {}, 'children': [{'element': 'plain/text', 'data': {}, 'attributes': {'textContent': 'Hello, {}'.format(username)}, 'children': []}]}]}]}}

@staticweb.route("/{username:get_user}/{this:that}")
def user_public(username, this):
	return staticweb.redirect("/gen/{}".format(username))

@staticweb.route("/file.json")
def datafile():
	return {"hello": "world"}

@staticweb.route("/file2.json")
def datafile2():
	return ["hello", "world"]

@staticweb.route("/staticfile.py")
def statfile():
	return staticweb.sendfile("example.py")

if __name__ == "__main__":
	staticweb.source(get_user=get_user, that=that)
	staticweb.compile()
	staticweb.run()

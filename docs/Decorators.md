# Decorators

These are functions exposed by `staticweb` that act as decorators in their normal usage.

## staticweb.route

This is the way of generating routes, allowing you to build a large number of pages from your data sources.

For example:

	@staticweb.route("/{username:get_user}/{this:that}")
	def user_public(username, this):
		return staticweb.redirect("/gen/{}".format(username))

## staticweb.HTMLView

This is a convenience constructor to turn a `dict` into a `HTMLResponse`, cleanly via a decorator.

For example:

	@staticweb.route("/gen/{username:get_user}")
	@staticweb.HTMLView()
	def gen_view(username):
		return {'doctype': 'html',
			'head': {'element': 'head', 'data': {}, 'attributes': {}, 'children': [
				{'element': 'meta', 'data': {}, 'attributes': {'charset': 'utf8'}, 'children': []}, {'element': 'meta', 'data': {}, 'attributes': {'content': 'width=device-width, initial-scale=1', 'name': 'viewport'}, 'children': []}, {'element': 'title', 'data': {}, 'attributes': {}, 'children': [{'element': 'plain/text', 'data': {}, 'attributes': {'textContent': 'Home'}, 'children': []}]}]},
			'body': {'element': 'body', 'data': {}, 'attributes': {}, 'children': [
				{'element': 'div', 'data': {}, 'attributes': {}, 'children': [{'element': 'p', 'data': {}, 'attributes': {}, 'children': [
					{'element': 'plain/text', 'data': {},
						'attributes': {
								'textContent': 'Hello, {}'.format(username)}, 'children': []}]}]}]}}


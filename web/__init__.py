import requests
import xml.etree.ElementTree as ET
import logging
from logging.handlers import SMTPHandler

from flask import jsonify, request
from flask_cors import CORS

from web.authorisation import generate_auth_token, auth_token_required
from sitetools.utility import (
	BetterExceptionFlask, disconnect_database, handle_exception,
	params_to_dict, authenticate_user, fetch_query, mutate_query
)

# instantiate the app
app = BetterExceptionFlask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = app.config['SECRETKEY']

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

if not app.debug:
	ADMINISTRATORS = [app.config['TO_EMAIL']]
	msg = 'Internal Error on reader'
	mail_handler = SMTPHandler(
		'127.0.0.1',
		app.config['FROM_EMAIL'],
		ADMINISTRATORS,
		msg
	)
	mail_handler.setLevel(logging.CRITICAL)
	app.logger.addHandler(mail_handler)


@app.errorhandler(500)
def internal_error(e):
	return handle_exception(), 500


@app.teardown_appcontext
def teardown(error):
	disconnect_database()


@app.route('/api/login', methods=['POST'])
def login():
	params = params_to_dict(request.json)

	userid = authenticate_user(params.get('username'), params.get('password'))

	if userid is not None:
		# success
		token = generate_auth_token(userid)
		return jsonify(token=token)

	# fail
	return jsonify(error='Login failed.'), 401


@app.route('/api/feeds', methods=['GET'])
@auth_token_required
def feeds(userid):
	items = fetch_query(
		"""
		SELECT
			fi.id, fi.name, fi.url, fi.description,
			fi.published, fi.image
		FROM feed_item fi
		LEFT JOIN feed f ON (f.id = fi.feedid)
		WHERE fi.read = false
		AND f.userid = %s
		ORDER BY fi.published DESC
		""",
		(userid,)
	)
	return jsonify(items)


@app.route('/api/feeds/refresh', methods=['GET'])
def feeds_refresh():
	feedlist = fetch_query("SELECT * FROM feed")
	for f in feedlist:
		resp = requests.get(f['url']).text
		tree = ET.fromstring(resp)[0]
		image = tree.find('image').find('url').text
		items = []
		for child in tree.findall('item'):
			item = {
				'feedid': f['id'],
				'name': child.find('title').text,
				'url': child.find('link').text,
				'description': child.find('description').text,
				'published': child.find('pubDate').text,
				'guid': child.find('guid').text,
				'image': image
			}
			items.append(item)

		mutate_query(
			"""
			INSERT INTO feed_item (
				feedid, name, url, description,
				published, guid, image
			) SELECT
				%(feedid)s, %(name)s, %(url)s, %(description)s,
				%(published)s, %(guid)s, %(image)s
			WHERE NOT EXISTS (
				SELECT 1 FROM feed_item WHERE feedid = %(feedid)s AND guid = %(guid)s
			)
			""",
			items,
			executemany=True
		)
	return jsonify()


if __name__ == '__main__':
	app.run()

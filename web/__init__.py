import requests
import xml.etree.ElementTree as ET
import logging
from logging.handlers import SMTPHandler

from flask import jsonify, request
from flask_cors import CORS

from web.authorisation import generate_auth_token, auth_token_required
from sitetools.utility import (
	BetterExceptionFlask, disconnect_database, handle_exception,
	params_to_dict, authenticate_user
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
	# fetch_query
	rss_url = 'https://goodbearcomics.com/feed/'
	resp = requests.get(rss_url).text
	tree = ET.fromstring(resp)[0]
	image = tree.find('image').find('url').text
	articles = []
	for child in tree.findall('item'):
		a = {
			'title': child.find('title').text,
			'link': child.find('link').text,
			'description': child.find('description').text,
			'published': child.find('pubDate').text,
			'guid': child.find('guid').text,
			'image': image
		}
		articles.append(a)
	return jsonify(articles)


if __name__ == '__main__':
	app.run()

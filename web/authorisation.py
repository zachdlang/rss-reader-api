# Standard library imports
from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt

# Third party imports
from flask import request, jsonify

# Local imports
from web import config
from sitetools.utility import fetch_query

LIFE_SPAN = timedelta(hours=1)


def _gen_token_payload(userid, lifespan, token_type):
	issued = datetime.now(timezone.utc)
	return {
		'iss': 'RSS-READER-API',
		'iat': issued,
		'exp': issued + timedelta(hours=1),
		'sub': userid,
		'token_type': token_type,
	}


def _validate_auth_token(token):
	try:
		payload = jwt.decode(token.encode(), config.SECRETKEY)
		userid = payload['sub']
	except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidTokenError):
		userid = None

	if userid is not None:
		existing = fetch_query(
			"SELECT * FROM app.enduser WHERE id = %s",
			(userid,),
			single_row=True
		)
		if existing:
			return userid
	return None


# Just using an auto token for now instead of auth/refresh combo
def generate_auth_token(userid):
	payload = _gen_token_payload(
		userid,
		timedelta(days=7),
		'bearer'
	)

	token = jwt.encode(payload, config.SECRETKEY)
	return token.decode()


def auth_token_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		userid = _validate_auth_token(request.headers.get('Authorization'))
		if userid is None:
			return jsonify('Unauthorized access.'), 401
		return f(userid, *args, **kwargs)

	return decorated_function

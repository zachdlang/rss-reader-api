#!/usr/bin/env python3

from web import app

app.run(
	debug=True,
	host='localhost',
	port=5000,
	threaded=True
)

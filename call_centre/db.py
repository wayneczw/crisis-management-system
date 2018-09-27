import os
import sqlite3
from flask import g, Flask


def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db


# commented because app is defined below
# @app.teardown_appcontext
# def close_connection(exception):
# 	db = getattr(g, '_database', None)
# 	if db is not None:
# 		db.close()


def init_db():
	with app.app_context():
		db = get_db()
		# assert db is not None
		with app.open_resource('schema.sql', mode = 'r') as f:
			db.cursor().executescript(f.read())
		db.commit()


if __name__ == '__main__':

	# just for testing purpose

	PATH = os.path.abspath('')
	DATABASE = os.path.join(PATH, 'database.db')
	# print(DATABASE)

	app = Flask(__name__, template_folder = "templates")

	init_db()
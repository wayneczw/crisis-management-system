# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session
from flask_googlemaps import GoogleMaps

from Dashboard.dashboard import dashboard_api
from AccountManagement.account_management import account_api
from Map.map import map_api

from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# create the application object
app = Flask(__name__)
app.secret_key = "aD1R3s2"
app.register_blueprint(dashboard_api)
app.register_blueprint(account_api, url_prefix='/account')
app.register_blueprint(map_api, url_prefix='/map')

# for google maps blueprint. not sure if this is a good design
API_KEY = "AIzaSyDc1Hx9zrh10qY4FSl-A0OwIVKRNTBkZGs"
app.config['GOOGLEMAPS_KEY'] = API_KEY
GoogleMaps(app, key=API_KEY)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'Dashboard.report:send_report',
            'args': None,
            'trigger': 'interval',
            'seconds': 60*30
        }
    ]

    SCHEDULER_API_ENABLED = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app.config.from_object(Config)

# db part
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import model

mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not __verify_login(request.form['username'], request.form['password'], request.form['role']):
            error = 'Invalid Credentials. Please try again.'
        else:
            session["logged_in"] = True
            session["username"] = request.form['username']
            return redirect(url_for('dashboard.dashboard'))
    return render_template('login-new.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))


def __verify_login(username, password, role):

    u = model.User().query.filter_by(username=username).first()

    if u.password == password and model.Role.query.filter_by(id=u.role_id).first().name == role:
        return True
    return False

    # string = '{},{},{}'.format(username, password, role)
    # userlist = open('db/userlist.csv').readlines()
    # for line in userlist:
    #     if string in line:
    #         return True
    # return False


# start the server with the 'run()' method
if __name__ == '__main__':

    # scheduler
    scheduler = APScheduler()
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    # turn off use reloader to prevent sending two duplicate emails
    app.run(debug=True, use_reloader=False)
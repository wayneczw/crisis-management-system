# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session
from flask_googlemaps import GoogleMaps

from Dashboard.dashboard import dashboard_api
from AccountManagement.account_management import account_api
from Map.map import map_api

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
    string = '{},{},{}'.format(username, password, role)
    userlist = open('db/userlist.csv').readlines()
    for line in userlist:
        if string in line:
            return True
    return False

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
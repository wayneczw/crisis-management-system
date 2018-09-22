# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from Dashboard.dashboard import dashboard_api
from Dashboard.account_management import account_api

# create the application object
app = Flask(__name__)
app.secret_key = "aD1R3s2"
app.register_blueprint(dashboard_api)
app.register_blueprint(account_api)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not __verify_login(request.form['username'], request.form['password'], request.form['role']):
            error = 'Invalid Credentials. Please try again.'
        else:
            session["logged_in"] = True
            return redirect(url_for('dashboard.dashboard'))
    return render_template('login-new.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out')
    return redirect(url_for('welcome'))


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
# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from Dashboard.dashboard import dashboard_api, dashboard

# create the application object
app = Flask(__name__)
app.secret_key = "aD1R3s2"
app.register_blueprint(dashboard_api)

# # login required decorator
# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash('You need to login first.')
#             return redirect(url_for('login'))
#     return wrap

# use decorators to link the function to a url
# @app.route('/dashboard')
# @login_required
# def home():
#     return render_template('dashboard.html')  # render a template

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        elif request.form['role'] != 'Admin':
            error = 'You are {}'.format(request.form['role'])
        else:
            session["logged_in"] = True
            flash('You were just logged in')
            return redirect(url_for('dashboard.dashboard'))
    return render_template('login-new.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out')
    return redirect(url_for('welcome'))

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
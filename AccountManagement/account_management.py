import os
import sqlite3

from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from werkzeug.exceptions import BadRequestKeyError

from utils import login_required

account_api = Blueprint('account', __name__, template_folder='templates')

from model import *
import re


@account_api.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """
    View function for registering users.

    Returns:
        render a template.
    """

    if request.method == "POST":
        new_username, new_password, new_role = request.form['hf-username'], request.form['hf-password'], request.form['select']
        status = register_user(new_username, new_password, new_role)
        if status == 0:
            flash("Username must contain 8 characters with small letters and numbers.")
        elif status == 1:
            flash('User - {} of role - {} is successfully created.'.format(new_username, new_role))
        elif status == 2:
            flash("Password must contain at least 10 characters with uppercase, lowercase letters and numbers.")
        else:
            flash("Register failed. User already exists.")

    return render_template('register.html')  # render a template


@account_api.route('/deregister', methods=['GET', 'POST'])
@login_required
def deregister():
    """
    View function for deregistering users.

    Returns:
        render a template.
    """
    if request.method == "POST":
        try:
            username, is_checked = request.form['username'], request.form['checkbox1']
            if deregister_user(username):
                flash('User - {} is successfully deregistered.'.format(username))
            else:
                flash('User does not exist. Please try again.')
        except BadRequestKeyError:
            flash('Please confirm that you want to deregister this account.')
    return render_template('deregister.html')  # render a template


def register_user(new_username, new_password, new_role):
    """
    Register a new user with validation.
    Username must contain 8 characters, small letters and numbers.
    Password must contain 10 characters, including big, small letters and numbers.

    Args:
        new_username: string of new username.
        new_password: string of password.
        new_role: choice of role.

    Returns:
         status code:
            0 -> Username violation
            1 -> OK
            2 -> Password violation
            3 -> Exception
    """
    # username must contain 8 characters, small letters and numbers
    if not re.match("^(?=.*[a-z])(?=.*\d)[a-z\d]{8}$", new_username):
        return 0        # username violation

    # password must contain 6-16 characters, including big, small letters and numbers
    elif not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,16}$", new_password):
        return 2        # password violation

    else:
        try:
            # u = User(username=new_username, password=new_password,
            #          role_id=Role.query.filter_by(name=new_role).first().id)
            # db.session.add(u)
            # db.session.commit()
            if __insert_user_to_db(new_username, new_password, 0):
                return 1    # OK
            else:
                return 3
        except Exception as e:
            print("register", e)
            return 3    # exception, user already exist


def deregister_user(username):
    """
    Deregister a user by username.

    Args:
        username: string of username.

    Returns:
        True for successful deregistration;
        False for unsuccessful deregistration.
    """
    try:
        # u = User.query.filter_by(username=username).first()
        # db.session.delete(u)
        # db.session.commit()
        return __delete_user_from_db(username)

    except Exception as e:
        return False    # exception, user does not exist


def __insert_user_to_db(name, password, role_id):
    script_path = os.path.dirname(os.path.abspath(__file__))
    db_path = '/'.join(script_path.split('/')[:-1]) + '/app.db'
    print(db_path)
    conn = sqlite3.connect(db_path)

    query = "INSERT INTO user (username, password, role_id) VALUES ('{}', '{}', '{}')".format(name, password, role_id)
    conn.execute(query)
    conn.commit()
    print('Insert user successfully!')
    conn.close()
    return True


def __delete_user_from_db(name):
    script_path = os.path.dirname(os.path.abspath(__file__))
    db_path = '/'.join(script_path.split('/')[:-1]) + '/app.db'
    print(db_path)
    conn = sqlite3.connect(db_path)

    query = "SELECT * FROM user WHERE username='{}'".format(name)
    user = conn.execute(query).fetchall()
    if len(user) > 0:
        query = "DELETE FROM user WHERE username='{}'".format(name)
        conn.execute(query)
        conn.commit()
        print('Deleted user successfully!')
        conn.close()
        return True

    else:
        return False

from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from werkzeug.exceptions import BadRequestKeyError

from utils import login_required

account_api = Blueprint('account', __name__, template_folder='templates')

from app import db
from model import User, Role


@account_api.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == "POST":
        new_username, new_password, new_role = request.form['hf-username'], request.form['hf-password'], request.form['select']
        __register_user(new_username, new_password, new_role)
        flash('User - {} of role - {} is successfully created.'.format(new_username, new_role))
    return render_template('register.html')  # render a template

@account_api.route('/deregister', methods=['GET', 'POST'])
@login_required
def deregister():
    if request.method == "POST":
        try:
            username, is_checked = request.form['username'], request.form['checkbox1']
            __deregister_user(username)
            flash('User - {} is successfully deregistered.'.format(username))
        except BadRequestKeyError:
            flash('Please confirm that you want to deregister this user!')
    return render_template('deregister.html')  # render a template


def __register_user(new_username, new_password, new_role):
    # open('db/userlist.csv', 'a+').write("{},{},{}\n".format(new_username, new_password, new_role))
    u = User(username=new_username, password=new_password,
             role_id=Role.query.filter_by(name=new_role).first().id)
    db.session.add(u)
    db.session.commit()


def __deregister_user(username):
    # userlist = open('db/userlist.csv').readlines()
    # for line in userlist:
    #     if username in line:
    #         userlist.remove(line)
    #         break
    # open('db/userlist.csv', 'w+').writelines(userlist)
    u = User.query.filter_by(username=username)
    db.session.delete(u)
    db.session.commit()

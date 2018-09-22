from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from Dashboard.utils import login_required

account_api = Blueprint('account', __name__, template_folder='templates')

@account_api.route('/register')
@login_required
def register():
    return render_template('register.html')  # render a template

@account_api.route('/deregister')
@login_required
def deregister():
    return render_template('deregister.html')  # render a template
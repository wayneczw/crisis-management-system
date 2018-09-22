from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from Dashboard.utils import login_required

dashboard_api = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_api.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')  # render a template


#
@dashboard_api.route('/deregister')
@login_required
def deregister():
    return render_template('deregister.html')  # render a template
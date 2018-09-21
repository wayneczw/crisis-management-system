from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from utils import login_required

dashboard_api = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_api.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')  # render a template
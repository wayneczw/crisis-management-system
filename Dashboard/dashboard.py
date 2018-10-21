from flask import render_template, redirect, url_for, request, session, flash, Blueprint, send_from_directory
from utils import login_required
from Dashboard.report import send_report, parse_table, get_latest_report, get_trend_values

dashboard_api = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard_api.route('/dashboard')
@login_required
def dashboard():
    psi, dengue = get_trend_values()
    return render_template('dashboard.html', psi=psi, dengue=dengue)  # render a template


from model import *
@dashboard_api.route('/report')
@login_required
def report():
    reports = Report.query.all()
    return render_template('report.html', reports=reports)


@dashboard_api.route("/download/<path>")
@login_required
def download(path=None):
    return send_from_directory('./Dashboard/report_history',
                               path, as_attachment=True)


@dashboard_api.route("/send_now")
@login_required
def send_now():
    send_report()
    flash("Sent successfully!")
    return redirect(url_for('dashboard.report'))
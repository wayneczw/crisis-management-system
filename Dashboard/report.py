from Map.map_api import get_weather, get_psi, get_dengue_clusters
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timezone
import os
import sqlite3
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
FOLDER_PATH = os.path.join(SCRIPT_PATH, 'report_history')

SENDER = '809955765@qq.com'
PASSWORD = 'uruirwekuirkbejf'
RECEIVERS = ['yue0068@gmail.com']

SUBJECT = "Status Report @ {0}"
TEMPLATE = '''\
       <html>
         <head></head>
         <body>
            <p>Dear Prime Minister,</p>
            <br>
            <p>The key indicators and trends at {0} are shown below:</p>
            <p><font color="red">{1}</font></p>
            <p>Please feel free to contact us if you need any further information.</p>
            <br>
            <p>Sincerely,</p>
            <p>Crisis Management System - Team Giligili</p>
            <p><i><small>Note: This is an automatically generated email.</small></i></p>

         </body>
       </html>
       '''
TABLE_CSS = """
            <style>
            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 40%;
            }

            td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            </style>
        """

# set up email server
server = smtplib.SMTP_SSL('smtp.qq.com', 465)
server.ehlo()
server.login(SENDER, PASSWORD)

DENGUE_SHORT_THRESHOLD = 3
DENGUE_LONG_THRESHOLD = 8


def get_latest_report(num=1):
    """

    Fetches latest n report from local directory. [crisis-management-system/Dashboard/report_history]

    Args:
        num: the number of report need to be fetched, default is 1

    Returns:
        report_path_list: a list of selected report absolute path

    """

    if not os.path.isdir(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)
    return [os.path.join(FOLDER_PATH, i) for i in sorted(os.listdir(FOLDER_PATH))[-num:]]


def parse_table(html_path, id):
    """

    Get selected table section from a html file.

    Args:
        html_path: path to html file
        id: id of table   ['psi', 'dengue', 'weather', 'incident']

    Returns:
        A string of selected table section

    """

    with open(html_path, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    bs = soup.find('table', id=id)

    results = {}
    for row in bs.findAll('tr')[1:]:
        aux = row.findAll('td')
        # remove (new), (+1), (-5)
        results[aux[0].get_text().replace('(new)', '')] = [aux[1].get_text().split('(')[0], aux[2].get_text().split('(')[0]]
    return results


def get_psi_report():
    """

    Generate psi html table report by calling psi API from map_api.py

    Args:

    Returns:
        psi_report: A string of psi html table report.

    """
    psi_dict = {'locality': [], 'psi': [], 'status': []}
    direction_list = ['east', 'west', 'sourth', 'north', 'central']
    for i, p in enumerate(get_psi()):
        psi_dict['locality'].append(direction_list[i])
        psi_dict['psi'].append(p['psi'])
        psi_dict['status'].append(p['status'])

    keys = list(psi_dict.keys())
    length = len(psi_dict[keys[0]])

    items = ['<table id="psi">', '<caption><h3>3. PSI Report</h3></caption>', '<tr>']
    for k in keys:
        items.append('<td><b>%s</b></td>' % k)
    items.append('</tr>')

    for i in range(length):
        items.append('<tr>')
        for k in keys:
            if k == 'locality':
                items.append('<td>%s</td>' % psi_dict[k][i])
                continue
            if psi_dict['status'][i] == 'Healthy':
                items.append('<td>%s</td>' % psi_dict[k][i])
            elif psi_dict['status'][i] == 'Moderate':
                items.append('<td><font color="yellow">%s</font></td>' % psi_dict[k][i])
            elif psi_dict['status'][i] == 'Unhealthy':
                items.append('<td><font color="orange">%s</font></td>' % psi_dict[k][i])
            else:
                items.append('<td><font color="red">%s</font></td>' % psi_dict[k][i])
        items.append('</tr>')

    items.append('</table>')

    psi_report = '\n'.join(items)
    return psi_report


def get_dengue_report():
    """

    Generate dengue html table report by calling psi API from map_api.py

    Args:

    Returns:
        dengue_report: A string of dengue html table report.

    """

    attrs = ['Case with onset in last 2 weeks', 'Cases since start of cluster']
    dengue_dict = {'locality': [], attrs[0]: [], attrs[1]: []}

    for d in get_dengue_clusters():
        dengue_dict['locality'].append(d['locality'])
        dengue_dict['Case with onset in last 2 weeks'].append(d['num_last2weeks'])
        dengue_dict['Cases since start of cluster'].append(d['num_all'])

    # get last report
    last_dengue = get_latest_report(1)
    # if last report exists
    if len(last_dengue) > 0:
        last_dengue_dict = parse_table(last_dengue[0], id='dengue')
        print(last_dengue_dict)

    keys = list(dengue_dict.keys())
    length = len(dengue_dict[keys[0]])

    # sort three list by first list order
    dengue_dict['locality'], dengue_dict[attrs[0]], dengue_dict[attrs[1]] = \
        zip(*sorted(zip(dengue_dict['locality'], dengue_dict[attrs[0]], dengue_dict[attrs[1]])))

    items = ['<table id="dengue">', '<caption><h3>1. Dengue Report</h3></caption>', '<tr>']
    for k in keys:
        items.append('<td><b>%s</b></td>' % k)
    items.append('</tr>')

    for i in range(length):
        items.append('<tr>')
        location = None
        for k in keys:
            if k == attrs[0] and int(dengue_dict[k][i]) >= DENGUE_SHORT_THRESHOLD or \
                    k == attrs[1] and int(dengue_dict[k][i]) >= DENGUE_LONG_THRESHOLD:
                color = "red"
            else:
                color = ""

            change_text = ""

            # if last dengue exits
            if len(last_dengue) > 0:
                # if it appears in last report, show change
                if location:
                    if k in attrs:
                        diff = int(dengue_dict[k][i]) - int(last_dengue_dict[location][attrs.index(k)])
                        # if decrease, show blue diff
                        if diff < 0:
                            change_text = '<font color="blue">({})</font>'.format(diff)
                        # if increase, show red diff
                        elif diff > 0:
                            change_text = '<font color="red">(+{})</font>'.format(diff)

                # if this is locality column
                if k not in attrs:
                    if dengue_dict[k][i] in last_dengue_dict.keys():
                        location = dengue_dict[k][i] # this location appear in last report
                    else:
                        # new locality, add red "(new)" next to this locality name
                        items.append('<td>{}<font color="red">(new)</font></td>'.format(dengue_dict[k][i]))
                        continue
            items.append('<td><font color="{}">{}</font>{}</td>'.format(color, dengue_dict[k][i], change_text))
        items.append('</tr>')

    items.append('</table>')

    dengue_report = '\n'.join(items)
    return dengue_report


def get_weather_report():
    """

    Generate weather html table report by calling psi API from map_api.py

    Args:

    Returns:
        weather_report: A string of weather html table report.

    """
    weather_dict = {'locality': [], 'weather': []}
    weather = get_weather()
    for w in weather:
        weather_dict['locality'].append(w)
        weather_dict['weather'].append(weather[w]['forecast'])

    keys = list(weather_dict.keys())
    length = len(weather_dict[keys[0]])

    items = ['<table id="weather">', '<caption><h3>2. Weather Report</h3></caption>', '<tr>']
    for k in keys:
        items.append('<td><b>%s</b></td>' % k)
    items.append('</tr>')

    for i in range(length):
        items.append('<tr>')
        for k in keys:
            if k == 'weather':
                if weather_dict[k][i] == 'Moderate Rain':
                    items.append('<td><font color="blue">%s</font></td>' % weather_dict[k][i])
                elif 'Heavy' in weather_dict[k][i] or 'Thundery' in weather_dict[k][i]:
                    items.append('<td><font color="red">%s</font></td>' % weather_dict[k][i])
                else:
                    items.append('<td>%s</td>' % weather_dict[k][i])
            else:
                items.append('<td>%s</td>' % weather_dict[k][i])
        items.append('</tr>')

    items.append('</table>')

    weather_report = '\n'.join(items)
    return weather_report


def retrieve_active_incident_reports():
    """

    Retrieve active incident report from /CallCenter/database.db

    Args:

    Returns:
        list_all_incident_reports: A list of all incident reports.

    """
    script_path = os.path.dirname(os.path.abspath(__file__))
    db_path = '/'.join(script_path.split('/')[:-1]) + '/CallCenter/database.db'
    print(db_path)
    conn = sqlite3.connect(db_path)

    all_incident_reports = conn.execute("SELECT * FROM INCIDENT_REPORT")

    assistance_required_dict = {0: 'No Assistance needed', 1: 'Emergency Ambulance', 2: 'Rescue and Evaluate',
                                3: 'Gas Leak Control'}  # a Dict to convert assistance_required from int to string
    report_status_dict = {1: 'REPORTED', 2: 'PENDING',
                          3: 'CLOSED'}  # a Dict to convert report_status required from int to string
    is_first_such_incident_dict = {0: 'FALSE',
                                   1: 'TRUE'}  # a Dict to convert is_first_such_incident from int to string

    list_all_incident_reports = []
    for report in all_incident_reports:
        report = list(report)  # Convert Tuple [1 Incident Report] into a list as list is easier to manipulate
        report[1] = report[1][
                    :-7]  # Remove the last 7 chars of the timestamp for "First reported time" as they are too precise.
        report[5] = assistance_required_dict[report[5]]  # Convert asssistance_required from int to string
        report[10] = report_status_dict[report[10]]  # Convert report_status from int to string
        report[11] = is_first_such_incident_dict[report[11]]  # Convert is_first_such_incident from int to string

        report = report[:12]  # Remove information on Latitude and Longitude as they are not needed
        list_all_incident_reports.append(report)

    return list_all_incident_reports


def get_incident_report():
    """

    Generate incident html table report by calling psi API from map_api.py

    Args:

    Returns:
        incident_report: A string of incident html table report.

    """

    incident_list = retrieve_active_incident_reports()
    print(incident_list)

    incident_dict = {'id': [], 'report date': [], 'reporter': [],
                     "report's HP": [], 'location': [],
                     'tyoe of assistance need': [], 'description': [],
                     'priority for severity of injuries': [],
                     'priority for impending dangers': [],
                     'priority for presence of nearyby help': [],
                     'status': []}

    keys = list(incident_dict.keys())

    for inc in incident_list:
        for i, attr in enumerate(inc[:11]):
            incident_dict[keys[i]].append(attr)

    length = len(incident_dict[keys[0]])

    items = ['<table id="incident">', '<caption><h3>4. Incident Report</h3></caption>', '<tr>']
    for k in keys:
        items.append('<td><b>%s</b></td>' % k)
    items.append('</tr>')

    for i in range(length):
        items.append('<tr>')
        for k in keys:
            items.append('<td>%s</td>' % incident_dict[k][i])
        items.append('</tr>')

    items.append('</table>')

    incident_report = '\n'.join(items)
    return incident_report


def insert_db(name, timestamp, path):
    """

    Insert status report into app.db.

    Args:
        name: name of  the status report
        timastamp: timastamp of the status report
        path: path of the status report

    Returns:
        Print after successful add.

    """
    script_path = os.path.dirname(os.path.abspath(__file__))
    db_path = '/'.join(script_path.split('/')[:-1])+'/app.db'
    conn = sqlite3.connect(db_path)

    query = "INSERT INTO report (NAME, TIMESTAMP, HTML_PATH) VALUES ('{}', '{}', '{}')".format(name, timestamp, path)
    conn.execute(query)
    conn.commit()
    print('Db saved successfully!')


def send_report(subject=SUBJECT):

    """

    0. Generate status report.
    1. Send status report to target email.
    2. Save status report to local directory.
    3. Insert status report into app.db.

    Args:
        subject: subject of the email

    Returns:
        Print after successful sending email / saving file / inserting database.

    Raises:
        Exception: An error occured in sending email / save local file / insert database.
    """

    try:
        now_time = datetime.now(timezone.utc).astimezone()
        now = now_time.strftime("%Y-%m-%d %H:%M:%S")
        subject = subject.format(now)

        content = '<br>'.join([TABLE_CSS, get_dengue_report(), get_weather_report(), get_psi_report(), get_incident_report()])

        email_content = TEMPLATE.format(now, content)

        msg_to = ""
        for person in RECEIVERS:
            msg_to += "{0} ".format(person)

        msg = MIMEText(email_content, 'html')

        msg['Subject'] = subject
        msg['From'] = SENDER
        msg['To'] = msg_to

        # send email
        server.sendmail(SENDER, RECEIVERS, msg.as_string())
        print('Sent successfully!')

        # save to local
        if not os.path.isdir(FOLDER_PATH):
            os.makedirs(FOLDER_PATH)
        file_path = "{}/report_history/{}.html".format(SCRIPT_PATH, subject)
        with open(file_path, "w") as fp:
            fp.write(email_content)
        print('File saved successfully!')

        # insert to db
        insert_db(subject, now_time, file_path.split('/')[-1])

    except Exception as e:
        print(e)
        return False


def get_trend_values():
    reports = get_latest_report(10)
    psi_trend, dengue_trend = {}, {}
    dengue_trend["2 weeks total"] = []
    dengue_trend["overall total"] = []
    for r in reports:
        cur_psi_report = parse_table(r, id="psi")

        # psi example: {'east': ['12', 'Healthy'], 'west': ['10', 'Healthy'], 'sourth': ['13', 'Healthy'],
        # 'north': ['10', 'Healthy'], 'central': ['11', 'Healthy']}

        cur_dengue_report = parse_table(r, id="dengue")

        # dengue example: {'Bishan Street 11(Bishan Loft)': ['3', '3'], 'Bukit Batok Street 21(Blk 201)': ['3', '3'],
        # 'Eng Kong Crescent': ['3', '5'], 'Jalan Gelenggang': ['2', '5'], 'Jalan Tenaga(Blk 656)': ['5', '6'],
        # 'Woodlands Avenue 5(Bellewoods)': ['3', '5'], 'Woodlands Circle': ['1', '10'], 'Woodlands Cresent(Blk 787C)': ['5', '5']}

        cur_incident_report = parse_table(r, id="incident")

        for key in cur_psi_report:
            if key not in psi_trend:
                psi_trend[key] = []
            psi_trend[key].append(int(cur_psi_report[key][0]))

        sum_two_weeks = 0
        sum_overall = 0
        for key in cur_dengue_report.keys():
            sum_two_weeks += int(cur_dengue_report[key][0])
            sum_overall += int(cur_dengue_report[key][1])

        dengue_trend["2 weeks total"].append(sum_two_weeks)
        dengue_trend["overall total"].append(sum_overall)

    return psi_trend, dengue_trend


def generate_trend_chart():
    '''
    Generate chart using the latest 10 reports.
    :return: chart - a chart image name
    '''
    psi, dengue = get_trend_values()
    linestyles = ['-', '--', '-.', ':', '-']
    for i in range(len(list(psi.keys()))):
        key = list(psi.keys())[i]
        plt.plot(range(len(psi[key])), psi[key], linestyle=linestyles[i], label=key)
        plt.scatter(range(len(psi[key])), psi[key])
        time_ticks = generate_time_ticks()
        plt.xticks(range(len(time_ticks)), time_ticks)
        plt.legend()
        plt.title('PSI trend for the past 5 hours')
    plt.savefig('report_history/PSI trend.png'.format(datetime.now()))
    plt.close()

    for key in dengue.keys():
        print(dengue[key])
        plt.plot(range(len(dengue[key])), dengue[key], label=key)
        plt.scatter(range(len(dengue[key])), dengue[key])
        plt.xticks(range(len(time_ticks)), time_ticks)
        plt.legend()
        plt.title('Dengue cases trend for the past 5 hours')
    plt.savefig('report_history/Dengue trend.png'.format(datetime.now()))
    plt.close()


def generate_time_ticks():
    '''
    Generate 10 time ticks.
    :return: list of 10 time ticks.
    '''
    current_time = datetime.now()
    current_hours = current_time.hour
    current_minutes = current_time.minute

    times = [];
    if 0 <= current_minutes <= 9:
        current_minutes = "0" + str(current_minutes)
    times.append(str(current_hours) + ":" + str(current_minutes))

    current_minutes = int(current_minutes)

    for i in range(9):
        current_minutes -= 30
        if current_minutes < 0:
            current_hours -= 1
            if current_hours < 0:
                current_hours += 24
            current_minutes += 60

        if 0 <= current_minutes <= 9:
            current_minutes = "0" + str(current_minutes)

        times.append(str(current_hours) + ":" + str(current_minutes))
        current_minutes = int(current_minutes)

    times.reverse()
    return times


if __name__ == '__main__':
    # for i in range(10):
    #     send_report()
    generate_trend_chart()


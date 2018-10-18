from Map.map_api import get_weather, get_psi, get_dengue_clusters
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timezone
import os
from CallCenter.CallCenter_Model import retrieve_active_incident_reports

def get_psi_report():
    psi_dict = {'locality': [], 'psi': [], 'status': []}
    direction_list = ['east', 'west', 'sourth', 'north', 'central']
    for i, p in enumerate(get_psi()):
        psi_dict['locality'].append(direction_list[i])
        psi_dict['psi'].append(p['psi'])
        psi_dict['status'].append(p['status'])

    keys = list(psi_dict.keys())
    length = len(psi_dict[keys[0]])

    items = ['<table>', '<caption><h3>3. PSI Report</h3></caption>', '<tr>']
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
    dengue_dict = {'locality': [], 'Case with onset in last 2 weeks': [], 'Cases since start of cluster': []}
    short_threshold = 3
    long_threshold = 8

    for d in get_dengue_clusters():
        dengue_dict['locality'].append(d['locality'])
        dengue_dict['Case with onset in last 2 weeks'].append(d['num_last2weeks'])
        dengue_dict['Cases since start of cluster'].append(d['num_all'])

    keys = list(dengue_dict.keys())
    length = len(dengue_dict[keys[0]])

    items = ['<table>', '<caption><h3>1. Dengue Report</h3></caption>', '<tr>']
    for k in keys:
        items.append('<td><b>%s</b></td>' % k)
    items.append('</tr>')

    for i in range(length):
        items.append('<tr>')
        for k in keys:
            if k == 'Case with onset in last 2 weeks' and int(dengue_dict[k][i]) >= short_threshold or \
                    k == 'Cases since start of cluster' and int(dengue_dict[k][i]) >= long_threshold:
                items.append('<td><font color="red">%s</font></td>' % dengue_dict[k][i])
            else:
                items.append('<td>%s</td>' % dengue_dict[k][i])
        items.append('</tr>')

    items.append('</table>')

    dengue_report = '\n'.join(items)
    return dengue_report


def get_weather_report():
    weather_dict = {'locality': [], 'weather': []}
    weather = get_weather()
    for w in weather:
        weather_dict['locality'].append(w)
        weather_dict['weather'].append(weather[w]['forecast'])

    keys = list(weather_dict.keys())
    length = len(weather_dict[keys[0]])

    items = ['<table>', '<caption><h3>2. Weather Report</h3></caption>', '<tr>']
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


def get_incident_report():

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

    items = ['<table>', '<caption><h3>4. Incident Report</h3></caption>', '<tr>']
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

SENDER = 'giligili.cms@gmail.com'
PASSWORD = 'giligili3002'
RECEIVERS = ['cms3002@googlegroups.com']

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
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(SENDER, PASSWORD)


def insert_db(name, timestamp, path):
    import sqlite3
    script_path = os.path.dirname(os.path.abspath(__file__))
    db_path = '/'.join(script_path.split('/')[:-1])+'/app.db'
    conn = sqlite3.connect(db_path)

    query = "INSERT INTO report (NAME, TIMESTAMP, HTML_PATH) VALUES ('{}', '{}', '{}')".format(name, timestamp, path)
    conn.execute(query)
    conn.commit()
    print('Db saved successfully!')


def send_report(subject=SUBJECT):

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

    # server.sendmail(SENDER, RECEIVERS, msg.as_string())
    # print('Sent successfully!')

    script_path = os.path.dirname(os.path.abspath(__file__))
    file_path = "{}/report_history/{}.html".format(script_path, subject)
    with open(file_path, "w") as fp:
        fp.write(email_content)
    print('File saved successfully!')

    insert_db(subject, now_time, file_path.split('/')[-1])


if __name__ == '__main__':
    send_report()



import os
import sqlite3
import json
from datetime import datetime, timedelta
from flask import g, Flask
from Map.map_api import address_to_latlng


# from CallCenter import app


PATH = os.path.abspath('')
DATABASE = os.path.join(PATH, 'database.db')
# print(DATABASE)

app = Flask(__name__, template_folder = "templates")

'''
Function:
    get_db
Args:
    No arguments
Returns:
    db: A reference to database
Raises:
    No exception
'''


def get_db():
    # getattr() will return the value of the '_database' attribute from g [see comment on g in the next line].
    # if g has no attribute called "_database", then 'None' is returned
    db = getattr(g, '_database',
                 None)  # g is a global/object that would last for only 1 request/response cycle [data in g does not persist, unlike a database]
    if db is None:
        db = g._database = sqlite3.connect(
                DATABASE)  # sqlite3.connect(DATABASE) will create the Database if that Database does not yet exist.
    return db

'''
Function:
    close_connection
Args:
    exception: the exception forces the disconnetion of controller and database
Returns:
    No return value
Raises:
    No exception
'''


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

'''
Function:
    init_db
Args:
    No arguments
Returns:
    No return value
Raises:
    FileNotFoundError
'''


def init_db():
    with app.app_context():  # Within flask's application context
        db = get_db()

        # Opens a resource from the application’s resource folder:
        with app.open_resource('schema.sql', mode = 'r') as f:
            # Cursor is an object that allow us to fetch multiple results from the database and keep track of which result is which.
            db.cursor().executescript(f.read())  # executescript allow us to execute "multiple SQL statements at once".
        db.commit()  # Tell the Database to confirm/finalise the changes made to it. No Changes to DB can be reverted back after commit() is called.

'''
Function:
    query_db
Args:
    query: an SQL query template
    args: a list of variables
Returns:
    return rv: the result of the exectued query
Raises:
    No
'''


def query_db(query, args = ()):
    cur = get_db().execute(query, args)  # cur is a Cursor object that contains the Results of the executed 'query'
    rv = cur.fetchall()  # retrieve the results from the Cursor object
    cur.close()  # close the cursor
    return rv


'''
Checks if the name is legal. If not a ValueError would be raised
'''

'''
Function:
    __check_name
Args:
    name: the name of the reporter
Returns:
    No return value
Raises:
    ValueError if the name is illegal
'''


def __check_name(name):
    if len(name) == 0:
        raise ValueError('name cannot be empty')
    for it in name:
        if 'A' <= it <= 'Z' or 'a' <= it <= 'z' or it == '.' or it == ' ' or it == ',' or it == '-':
            continue
        raise ValueError('Illegal character ' + it + ' in name')


'''
Checks if the mobile number is legal
The legal ones are defined as: [country code][' '|'-'][number]
Country code is either started by a '+' and followed by 1-3 digits or 4 digits
Number is defined as 8 to 13 digits.
'''

'''
Function:
    __check_mobile_no
Args:
    no : the phone number of the reporter
Returns:
    No return value
Raises:
    ValueError if the mobile number is illegal
'''

def __check_mobile_no(no):
    if len(no) == 0:
        raise ValueError('mobile number cannot be empty')

    no = no.split()
    if len(no) == 1:
        no = no[0].split('-')

    if len(no) > 2:
        raise ValueError('Too many spaces or hyphens :(')

    if len(no) == 1:
        if len(no[0]) < 7 or len(no[0]) > 14:
            raise ValueError('The number is either too short or too long')
        for it in no[0]:
            if it < '0' or it > '9':
                raise ValueError('The number should be numerical')
    else:
        if len(no[0]) > 4 or len(no[0]) == 0:
            raise ValueError('Illegal country code')
        if no[0][0] == '+':
            if len(no[0]) > 4 or len(no[0]) < 2:
                raise ValueError('Illegal country code')
            for i in range(1, len(no[0])):
                if no[0][i] < '0' or no[0][i] > '9':
                    raise ValueError('Illegal country code')
        else:
            if len(no[0]) != 4:
                raise ValueError('Illegal country code')

        if len(no[1]) < 7 or len(no[1]) > 14:
            raise ValueError('The number is either too short or too long')
        for it in no[1]:
            if it < '0' or it > '9':
                raise ValueError('The number should be numerical')


'''
Check if the location is empty.
'''

'''
Function:
    __check_loc
Args:
    loc : the location of the incident reported
Returns:
    No return value
Raises:
    ValueError if the location is empty
'''


def __check_loc(loc):
    loc = str(loc)
    if len(loc) == 0:
        raise ValueError('location cannot be empty')


'''
Check if the description is empty
'''

'''
Function:
    __check_description
Args:
    description : the description of the incident reported
Returns:
    No return value
Raises:
    ValueError if the description is empty
'''


def __check_description(description):
    if len(description) == 0:
        raise ValueError('description cannot be empty')


'''
Private method
The same report judgement is buggy and I have no idea how to fix it
The current assumption is the first reported case would always report the earliest time...
'''

'''
Function:
    __insert_incident
Args:
    name, mobile_number, location, assistance_required, description, priority_injuries,
    priority_dangers, priority_help, report_status,report_time: information of an incident kept in database
Returns:
    _id : the id of the newest inserted report
Raises:
    No exception
'''


def __insert_incident(name, mobile_number, location, assistance_required, description, priority_injuries,
                      priority_dangers, priority_help, report_status,
                      report_time, latitude, longitude):
    # creating a time interval that another new incident report would be classified as being about the same incident as this current incident report.
    earliest_time = report_time - timedelta(minutes = 5)

    with app.app_context():  # Within the Application Context:
        db = get_db()  # call our private method to retreive the DB

        # Checking if the Incident has already been reported before
        similar_incident_reports = query_db(
                '''
                SELECT id FROM INCIDENT_REPORT WHERE
                location = ? AND
                priority_injuries = ? AND
                priority_dangers = ? AND
                priority_help = ? AND
                assistance_required = ? AND
                first_reported > ?
                ''',
                [
                    location,
                    priority_injuries,
                    priority_dangers,
                    priority_help,
                    assistance_required,
                    earliest_time
                ]
        )

        # If not such Incident has been reported before, Insert an Incident Report into DB
        if len(similar_incident_reports) == 0:
            is_first_such_incident = 1  # True

        else:  # If the Incident Report pertains to an Incident which has already been reported.
            is_first_such_incident = 0  # False

        query_db(
                '''
                INSERT INTO INCIDENT_REPORT(
                  name,
                  location,
                  priority_injuries,
                  priority_dangers,
                  priority_help,
                  assistance_required,
                  first_reported,
                  mobile_number,
                  description,
                  report_status,
                  is_first_such_incident,
                  latitude,
                  longitude
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
                ''',
                [
                    name,
                    location,
                    priority_injuries,
                    priority_dangers,
                    priority_help,
                    assistance_required,
                    report_time,
                    mobile_number,
                    description,
                    report_status,
                    is_first_such_incident,
                    latitude,
                    longitude]
        )

        # Retrieve the id of the Incident Report that we have just inserted into the DB [The id is set by the DB]
        _id = query_db(
                '''
                SELECT id FROM INCIDENT_REPORT WHERE
                location = ? AND
                priority_injuries = ? AND
                priority_dangers = ? AND
                priority_help = ? AND
                assistance_required = ? AND
                first_reported = ?
                ''',
                [
                    location,
                    priority_injuries,
                    priority_dangers,
                    priority_help,
                    assistance_required,
                    report_time
                ]
        )

        db.commit()  # Confirm the changes made to the DB

        return _id  # Return the id of the Newly inserted Incident Report


'''
Function:
    insert_report
Args:
    name, mobile_number, location, assistance_required, description, priority_injuries, priority_dangers,
    priority_help, report_status: information of an incident to be kept in database
Returns:
    return 0
Raises:
        ValueError in __check_name raised if the name is illegal
        ValueError in __check_mobile_no raised if the mobile number is illegal
        ValueError in __check_loc raised if the location in empty
        ValueError in __check_description raised if the description is empty
        ValueError in insert_report raised if the report type and asssistance type are inconsistent
        AssertionError raised if the data inserted is invalid
        PermissionError raised if the reported incident is duplicated

'''


def insert_report(name, mobile_number, location, assistance_required, description, priority_injuries, priority_dangers,
                  priority_help, report_status):
    __check_name(name)
    __check_mobile_no(mobile_number)
    __check_loc(location)
    __check_description(description)

    # assistance_required is an int: 0 = No Assistance required; 1 = Emergency Ambulance; 2 = Rescue and Evacuation; 3 = Gas Leak Control
    # report_status is an int: 1 = REPORTED [No assistance required]; 2 = PENDING [Waiting for Assistance but Assistance has not reached the victim yet]; 3 = CLOSED [Assistance has reached the victim already]

    # Convert some string parameters into integers:
    assistance_required = int(assistance_required)
    priority_injuries = int(priority_injuries)
    priority_dangers = int(priority_dangers)
    priority_help = int(priority_help)
    report_status = int(report_status)

    if report_status == 1 and assistance_required != 0:
        raise ValueError('Inconsistent report type and assistance type')

    if report_status != 1 and assistance_required == 0:
        raise ValueError('Inconsistent report type and assistance type')

    # Checking the validity of the Data:
    assert -1 < assistance_required < 4
    assert 0 < priority_injuries < 11
    assert 0 < priority_dangers < 11
    assert 0 < priority_help < 11
    assert 0 < report_status < 4

    report_time = datetime.now()

    _dict = address_to_latlng(location)
    latitude = _dict['lat']
    longitude = _dict['lng']

    with app.app_context():
        db = get_db()
        duplicates = query_db(
                '''
                    SELECT * FROM INCIDENT_REPORT WHERE
                    first_reported > ? AND
                    location = ? AND
                    mobile_number = ? AND
                    assistance_required = ? AND
                    priority_injuries = ? AND
                    priority_dangers = ? AND
                    priority_help = ? AND
                    report_status = ?
                ''',
                [
                    report_time - timedelta(minutes = 5),
                    location,
                    mobile_number,
                    assistance_required,
                    priority_injuries,
                    priority_dangers,
                    priority_help,
                    report_status
                ]
        )
        if duplicates:
            raise PermissionError('Insertion forbidden.')

    incident_report_id = __insert_incident(name, mobile_number, location, assistance_required, description,
                                           priority_injuries, priority_dangers, priority_help, report_status,
                                           report_time, latitude, longitude)

    print(incident_report_id)

    return 0


'''
Function:
    delete_report
Args:
    id_of_incident_report : id of the incident report that would be deleted
Returns:
    return 0
Raises:
    No exception
'''


def delete_report(id_of_incident_report):
    with app.app_context():  # Within the Application Context:
        db = get_db()  # call our private method to retreive the DB
        query_db(
                '''
                DELETE FROM INCIDENT_REPORT WHERE
                id = ?
                ''',
                [
                    id_of_incident_report
                ]
        )
        db.commit()

    return 0


'''
Function:
    update_report
Args:
    id_of_incident_report, caller_name, caller_mobile_number, caller_location, type_of_assistance,
    description, priority_for_severity_of_injuries, priority_for_impending_dangers,
    priority_for_presence_of_nearby_help, report_status, is_first_such_incident: information of an incident kept in database
Returns:
    return 0
Raises:
    ValueError in __check_name raised if the name is illegal
    ValueError in __check_mobile_no raised if the mobile number is illegal
    ValueError in __check_loc raised if the location in empty
    ValueError in __check_description raised if the description is empty
    ValueError in update_report raised if the report type and asssistance type are inconsistent
'''


def update_report(id_of_incident_report, caller_name, caller_mobile_number, caller_location, type_of_assistance,
                  description, priority_for_severity_of_injuries, priority_for_impending_dangers,
                  priority_for_presence_of_nearby_help, report_status, is_first_such_incident):
    # assistance_required is an int: 0 = No Assistance required; 1 = Emergency Ambulance; 2 = Rescue and Evacuation; 3 = Gas Leak Control
    # report_status is an int: 1 = REPORTED [No assistance required]; 2 = PENDING [Waiting for Assistance but Assistance has not reached the victim yet]; 3 = CLOSED [Assistance has reached the victim already]

    __check_name(caller_name)
    __check_mobile_no(caller_mobile_number)
    __check_loc(caller_location)
    __check_description(description)

    if report_status == 1 and type_of_assistance != 0:
        raise ValueError('Inconsistent report type and assistance type')

    if report_status != 1 and type_of_assistance == 0:
        raise ValueError('Inconsistent report type and assistance type')

    with app.app_context():  # Within the Application Context:
        db = get_db()  # call our private method to retreive the DB

        query_db(
                '''
                UPDATE INCIDENT_REPORT SET
                  name = ?,
                  location = ?,
                  priority_injuries = ?,
                  priority_dangers = ?,
                  priority_help = ?,
                  assistance_required = ?,
                  mobile_number = ?,
                  description = ?,
                  report_status = ?,
                  is_first_such_incident = ?
                  WHERE id = ?
                ''',
                [
                    caller_name,
                    caller_location,
                    priority_for_severity_of_injuries,
                    priority_for_impending_dangers,
                    priority_for_presence_of_nearby_help,
                    type_of_assistance,
                    caller_mobile_number,
                    description,
                    report_status,
                    is_first_such_incident,
                    id_of_incident_report
                ]
        )

        db.commit()  # Confirm the changes made to the DB

    return 0


'''
Function:
    retrieve_all_incident_reports
Args:
    no arguments
Returns:
    list_all_incident_reports : get all the incident reports
Raises:
    No exception
'''


def retrieve_all_incident_reports():
    with app.app_context():  # Within the Application Context:
        db = get_db()  # call our private method to retreive the DB

        all_incident_reports = query_db(
                '''
                SELECT * FROM INCIDENT_REPORT
                '''
        )

        # Some Formatting of the results from the Database
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

        db.commit()  # Confirm the changes made to the DB

        return list_all_incident_reports


'''
Function:
    retrieve_active_incident_reports
Args:
    no arguments
Returns:
    list_all_active_incident_reports : get all the incident reports that are 'PENDING', i.e. awaiting assistance
Raises:
    No exception
'''


def retrieve_active_incident_reports():
    with app.app_context():  # Within the Application Context:
        db = get_db()  # call our private method to retreive the DB

        all_incident_reports = query_db(
                '''
                SELECT * FROM INCIDENT_REPORT WHERE
                report_status <= 2
                '''
        )

        # Some Formatting of the results from the Database
        assistance_required_dict = {0: 'No Assistance needed', 1: 'Emergency Ambulance', 2: 'Rescue and Evaluate',
                                    3: 'Gas Leak Control'}  # a Dict to convert assistance_required from int to string
        report_status_dict = {1: 'REPORTED', 2: 'PENDING',
                              3: 'CLOSED'}  # a Dict to convert report_status required from int to string
        is_first_such_incident_dict = {0: 'FALSE',
                                       1: 'TRUE'}  # a Dict to convert is_first_such_incident from int to string

        list_all_active_incident_reports = []
        for report in all_incident_reports:
            report = list(report)  # Convert Tuple [1 Incident Report] into a list as list is easier to manipulate
            report[1] = report[1][
                        :-7]  # Remove the last 7 chars of the timestamp for "First reported time" as they are too precise.
            report[5] = assistance_required_dict[report[5]]  # Convert asssistance_required from int to string
            report[10] = report_status_dict[report[10]]  # Convert report_status from int to string
            report[11] = is_first_such_incident_dict[report[11]]  # Convert is_first_such_incident from int to string

            list_all_active_incident_reports.append(report)

        db.commit()  # Confirm the changes made to the DB

        return list_all_active_incident_reports


'''
Function:
    retrieve_selected_incident_reports
Args:
    id_of_incident_report : the id of the incident that is being searched
Returns:
    report : the report that is being searched
Raises:
    No exception
'''


def retrieve_selected_incident_report(id_of_incident_report):
    with app.app_context():  # Within the Application Context:
        db = get_db()  # call our private method to retreive the DB

        report = query_db(
                '''
                SELECT * FROM INCIDENT_REPORT WHERE
                id = ?
                ''',
                [id_of_incident_report]
        )

        # Some Formatting of the results from the Database
        assistance_required_dict = {0: 'No Assistance needed', 1: 'Emergency Ambulance', 2: 'Rescue and Evaluate',
                                    3: 'Gas Leak Control'}  # a Dict to convert assistance_required from int to string
        report_status_dict = {1: 'REPORTED', 2: 'PENDING',
                              3: 'CLOSED'}  # a Dict to convert report_status required from int to string
        is_first_such_incident_dict = {0: 'FALSE',
                                       1: 'TRUE'}  # a Dict to convert is_first_such_incident from int to string

        report = report[0]  # get the report out from a list with just 1 element
        report = list(report)  # Convert Tuple [1 Incident Report] into a list as list is easier to manipulate
        report[1] = report[1][
                    :-7]  # Remove the last 7 chars of the timestamp for "First reported time" as they are too precise.
        report[5] = assistance_required_dict[report[5]]  # Convert asssistance_required from int to string
        report[10] = report_status_dict[report[10]]  # Convert report_status from int to string
        report[11] = is_first_such_incident_dict[report[11]]  # Convert is_first_such_incident from int to string

        db.commit()  # Confirm the changes made to the DB

        return report


'''
This function is to be called by dashboard
The two arguments are of datetime data type
If omitted, the default query would be of interval [now - 30min, now]
A list of json objects would be returned
'''

'''
Function:
    query_time_interval
Args:
    start : start time of the query
    end : end time of the query
Returns:
    ret : a list of json objects
Raises:
    No exception
'''


def query_time_interval(start = datetime.now() - timedelta(minutes = 30), end = datetime.now()):
    with app.app_context():
        res = query_db(
                'SELECT * FROM INCIDENT WHERE first_reported < ? AND first_reported > ?',
                [end, start]
        )

        # The priorities are currently returned as ints
        # Maybe they would be returned as strings to make more sense (but harder to handle) later

        ret = []
        for it in res:
            now = {
                'id'                 : it[0],
                'name'               : it[1],
                'first_reported'     : it[2],
                'location'           : it[3],
                'report_cnt'         : it[4],
                'priority_injuries'  : it[5],
                'priority_dangers'   : it[6],
                'priority_help'      : it[7],
                'assistance_required': it[8]
            }
            now = json.dumps(now)
            ret.append(now)

        return ret

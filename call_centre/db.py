import os
import sqlite3
import json
from datetime import datetime, timedelta
from flask import g, Flask


# from CallCenter import app


PATH = os.path.abspath('')
DATABASE = os.path.join(PATH, 'database.db')
# print(DATABASE)

app = Flask(__name__, template_folder = "templates")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        # assert db is not None
        with app.open_resource('schema.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args = (), one = False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


'''
Private method
The type of the argument should be either a string or a type convertible to string 
'''


def __insert_phone_number(number):
    try:
        number = str(number)
    except TypeError:
        return -1

    # get app context
    with app.app_context():
        db = get_db()

        now = query_db('SELECT * FROM CONTACT WHERE number = ?', [number], one = True)

        # duplicates
        if now is not None:
            return -1

        query_db('INSERT INTO CONTACT(number) VALUES (?)', [number])
        now = query_db('SELECT id FROM CONTACT WHERE number = ?', [number], one = True)
        assert now is not None
        db.commit()

        return now[0]


'''
Private method
The same report judgement is buggy and I have no idea how to fix it
The current assumption is the first reported case would always report the earliest time...
'''


def __insert_incident(name, location, priority_injuries, priority_dangers, priority_help, assistance_required,
                      report_time = datetime.now()):
    min_time = report_time - timedelta(minutes = 5)
    max_time = report_time + timedelta(minutes = 5)

    with app.app_context():
        db = get_db()
        now = query_db(
                '''
                SELECT id FROM INCIDENT WHERE 
                location = ? AND
                priority_injuries = ? AND
                priority_dangers = ? AND
                priority_help = ? AND
                assistance_required = ? AND
                first_reported > ? AND
                first_reported < ?
                ''',
                [
                    location,
                    priority_injuries,
                    priority_dangers,
                    priority_help,
                    assistance_required,
                    min_time,
                    max_time
                ]
        )

        # I don't know how to handle the case where 2 or more matches are found
        assert len(now) < 2

        # if now is not None:
        #     print(now)

        if len(now) == 0:
            # print('!')
            query_db(
                    '''
                    INSERT INTO INCIDENT(
                      name,
                      location,
                      priority_injuries,
                      priority_dangers,
                      priority_help,
                      assistance_required,
                      first_reported
                    ) VALUES (?, ?, ?, ?, ?, ?, ?) 
                    ''',
                    [
                        name,
                        location,
                        priority_injuries,
                        priority_dangers,
                        priority_help,
                        assistance_required,
                        report_time
                    ]
            )
            now = query_db(
                    '''
                    SELECT id FROM INCIDENT WHERE
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
                    ],
                    one = True
            )
        else:
            query_db('UPDATE INCIDENT SET report_cnt = report_cnt + 1 WHERE id = ?', now[0])

        db.commit()

        return now[0]


'''
I am not sure whether this should be private or public at this stage
'''


def insert_report(number, name, location, priority_injuries, priority_dangers, priority_help, assistance_required,
                  report_time = datetime.now()):
    assert 0 < priority_injuries < 4
    assert 0 < priority_dangers < 4
    assert 0 < priority_help < 4

    # assertion for assistance_required

    cid = __insert_phone_number(number)
    if cid == -1:
        return -1

    iid = __insert_incident(name, location, priority_injuries, priority_dangers, priority_help, assistance_required,
                            report_time)
    if iid == -1:
        return -1

    with app.app_context():
        db = get_db()

        if type(cid) is tuple:
            cid = cid[0]
        if type(iid) is tuple:
            iid = iid[0]

        # print(cid, iid)

        now = query_db('SELECT * FROM REPORT WHERE cid = ? AND iid = ?', [cid, iid], one = True)
        if now is not None:
            return -1

        query_db('INSERT INTO REPORT(cid, iid) VALUES (?, ?)', [cid, iid])

        db.commit()

    return 0


'''
This function is to be called by dashboard
The two arguments are of datetime data type
If omitted, the default query would be of interval [now - 30min, now]
A list of json objects would be returned
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

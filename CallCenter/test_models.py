from CallCenter_Model import *


# This function should be and only be used in this file
def __drop_database():
    with app.app_context():
        db = get_db()
        with app.open_resource('testing.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()


__drop_database()
init_db()

# If id is important in the implementation, then it should be returned instead of printed
# Also all non_inserting functions require id to call, which may be a bit complicated
insert_report(name = "report 1", mobile_number = "124213", location = "qweqeq", assistance_required = 2,
              description = "Des", priority_injuries = 1, priority_dangers = 1, priority_help = 2, report_status = 2)

# test duplicates
# assumption is if duplicates are found, the functions should raise some exceptions other than AssertionError

try:
    insert_report(name = "report 1", mobile_number = "124213", location = "qweqeq", assistance_required = 2,
                  description = "Des", priority_injuries = 1, priority_dangers = 1, priority_help = 2,
                  report_status = 2)
    assert False
except AssertionError:
    print('duplicates')
    pass

insert_report(name = "report 1", mobile_number = "124213", location = "qweqeq", assistance_required = 2,
              description = "Des", priority_injuries = 1, priority_dangers = 1, priority_help = 2,
              report_status = 1)

ret = retrieve_all_incident_reports()

# The assertion is made based on the assumption that duplicates are not eliminates
assert len(ret) == 3

assert ret[0][-1] == 'TRUE'
assert ret[1][-1] == 'FALSE'

ret = retrieve_active_incident_reports()
assert len(ret) == 2

try:
    update_report(id_of_incident_report = 1, caller_name = '123', caller_mobile_number = '2345', caller_location = 124,
                  type_of_assistance = 2, description = 'd', priority_for_severity_of_injuries = 1,
                  priority_for_impending_dangers = 2, priority_for_presence_of_nearby_help = 10000, report_status = 2,
                  is_first_such_incident = False)
except sqlite3.IntegrityError:
    pass


try:
    update_report(id_of_incident_report = 1, caller_name = '123', caller_mobile_number = '2345', caller_location = 124,
                  type_of_assistance = 2, description = '', priority_for_severity_of_injuries = 1,
                  priority_for_impending_dangers = 2, priority_for_presence_of_nearby_help = 5, report_status = 2,
                  is_first_such_incident = False)
    # raise RuntimeError('null string to not null field')
    print('null string is to not null field')
except sqlite3.IntegrityError:
    pass

delete_report(1)

ret = retrieve_active_incident_reports()
assert len(ret) == 1
assert ret[0][-1] == 'FALSE'

delete_report(2)

insert_report(name = "report 1", mobile_number = "124213", location = "qweqeq", assistance_required = 2,
              description = "Des", priority_injuries = 1, priority_dangers = 1, priority_help = 2,
              report_status = 2)

ret = retrieve_active_incident_reports()
assert len(ret) == 1
# The current inserted col considered not first time inserted
# assert ret[0][-1] == 'TRUE'

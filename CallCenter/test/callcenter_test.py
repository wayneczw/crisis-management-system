from CallCenter_Model import *
from unittest import TestCase, main
from time import sleep


# This function should be and only be used in this file
def __drop_database():
    with app.app_context():
        db = get_db()
        with app.open_resource('testing.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# __drop_database()
# init_db()

# If id is important in the implementation, then it should be returned instead of printed
# Also all non_inserting functions require id to call, which may be a bit complicated
# insert_report(name = "report This", mobile_number = "12421313", location = "qweqeq", assistance_required = 2,
#               description = "Des", priority_injuries = 1, priority_dangers = 1, priority_help = 2, report_status = 2)

# test duplicates
# assumption is if duplicates are found, the functions should raise some exceptions other than AssertionError

# try:
#     insert_report(name = "report This", mobile_number = "12421313", location = "qweqeq", assistance_required = 2,
#                   description = "Des", priority_injuries = 1, priority_dangers = 1, priority_help = 2,
#                   report_status = 2)
#     assert False
# except PermissionError as e:
#     print(e, end = '**\n')


# insert_report(name = "report This", mobile_number = "12421313", location = "qweqeq", assistance_required = 2,
#               description = "Des", priority_injuries = 1, priority_dangers = 1, priority_help = 2,
#               report_status = 3)
#
# ret = retrieve_all_incident_reports()
#
# assert len(ret) == 2
#
# assert ret[0][-1] == 'TRUE'
# assert ret[1][-1] == 'FALSE'
#
# ret = retrieve_active_incident_reports()
# assert len(ret) == 1
#
# try:
#     update_report(id_of_incident_report = 1, caller_name = 'This is-a proper name', caller_mobile_number = '23452345', caller_location = 124,
#                   type_of_assistance = 2, description = 'd', priority_for_severity_of_injuries = 1,
#                   priority_for_impending_dangers = 2, priority_for_presence_of_nearby_help = 10000, report_status = 2,
#                   is_first_such_incident = False)
# except sqlite3.IntegrityError:
#     pass
#
#
# try:
#     update_report(id_of_incident_report = 1, caller_name = 'This is-a proper name', caller_mobile_number = '23452345', caller_location = 124,
#                   type_of_assistance = 2, description = '', priority_for_severity_of_injuries = 1,
#                   priority_for_impending_dangers = 2, priority_for_presence_of_nearby_help = 5, report_status = 2,
#                   is_first_such_incident = False)
#     raise RuntimeError('null string to not null field')
#     # print('null string is to not null field')
# except ValueError as e:
#     print(e, end = '**\n')
#
# delete_report(1)
#
# ret = retrieve_active_incident_reports()
# assert len(ret) == 0
#
# delete_report(2)
#
# insert_report(name = "report This", mobile_number = "12421313", location = "qweqeq", assistance_required = 2,
#               description = "Des", priority_injuries = 1, priority_dangers = 1, priority_help = 2,
#               report_status = 2)
#
# ret = retrieve_active_incident_reports()
# assert len(ret) == 1
# The current inserted col considered not first time inserted
# assert ret[0][-1] == 'TRUE'


class TestIncidentReport(TestCase):

    def test_insert_incident_report(self):
        insert_report(
                name = 'Jiayun',
                mobile_number = '12345678',
                location = 'hall 6',
                assistance_required = 0,
                description = 'description',
                priority_injuries = 1,
                priority_dangers = 1,
                priority_help = 1,
                report_status = 1
        )

        try:
            insert_report(
                    name = '12345678',
                    mobile_number = '12345678',
                    location = 'hall 6',
                    assistance_required = 0,
                    description = 'description',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 1
            )
            raise AssertionError('name cannot be numerical')
        except ValueError:
            pass

        try:
            insert_report(
                    name = '',
                    mobile_number = '12345678',
                    location = 'hall 6',
                    assistance_required = 0,
                    description = 'description',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 1
            )
            raise AssertionError('name cannot be empty')
        except ValueError:
            pass

        try:
            insert_report(
                    name = 'Jiayun',
                    mobile_number = 'Jiayun',
                    location = 'hall 6',
                    assistance_required = 0,
                    description = 'description',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 1
            )
            raise AssertionError('mobile number cannot contain letters')
        except ValueError:
            pass

        try:
            insert_report(
                    name = 'Jiayun',
                    mobile_number = '',
                    location = 'hall 6',
                    assistance_required = 0,
                    description = 'description',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 1
            )
            raise AssertionError('mobile number cannot be empty')
        except ValueError:
            pass

        try:
            insert_report(
                    name = 'Jiayun',
                    mobile_number = '12345678',
                    location = '',
                    assistance_required = 0,
                    description = 'description',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 1
            )
            raise AssertionError('location cannot be empty')
        except ValueError:
            pass

        try:
            insert_report(
                    name = 'Jiayun',
                    mobile_number = '12345678',
                    location = 'hall 6',
                    assistance_required = 0,
                    description = '',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 1
            )
            raise AssertionError('description cannot be empty')
        except ValueError:
            pass

        try:
            insert_report(
                    name = 'Jiayun',
                    mobile_number = '12345678',
                    location = 'hall 6',
                    assistance_required = 1,
                    description = '',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 1
            )
            raise AssertionError('Inconsistent report type and assistance type')
        except ValueError:
            pass

        try:
            insert_report(
                    name = 'Jiayun',
                    mobile_number = '12345678',
                    location = 'hall 6',
                    assistance_required = 0,
                    description = '',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 0
            )
            raise AssertionError('Inconsistent report type and assistance type')
        except ValueError:
            pass

        try:
            insert_report(
                    name = 'Jiayun',
                    mobile_number = '12345678',
                    location = 'hall 6',
                    assistance_required = 0,
                    description = 'description',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 1
            )
            raise AssertionError('Duplicates!!!')
        except PermissionError:
            pass

        insert_report(
                    name = 'abc',
                    mobile_number = '87654321',
                    location = 'hall 6',
                    assistance_required = 0,
                    description = 'description',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 1
            )

        sleep(5)
        update_report(
                    id_of_incident_report = 1,
                    caller_name = 'Jiayunnnnn',
                    caller_mobile_number = '12345678',
                    caller_location = 'hall 6',
                    type_of_assistance = 0,
                    description = 'description',
                    priority_for_severity_of_injuries = 1,
                    priority_for_impending_dangers = 1,
                    priority_for_presence_of_nearby_help = 1,
                    report_status = 1,
                    is_first_such_incident = 1
            )


if __name__ == '__main__':
    __drop_database()
    init_db()

    main()

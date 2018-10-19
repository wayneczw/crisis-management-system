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

    def test_retrieve_incident_report(self):

        insert_report(
                name = 'Jia Yun',
                mobile_number = '+65 12345678',
                location = 'hall 14',
                assistance_required = 1,
                description = 'description',
                priority_injuries = 1,
                priority_dangers = 1,
                priority_help = 1,
                report_status = 2
        )

        now = retrieve_all_incident_reports()
        assert len(now) == 3
        now = retrieve_active_incident_reports()
        assert len(now) == 3
        # The name is unique so we can make assertion on it
        assert now[-1][2] == 'Jia Yun'

        now = retrieve_all_incident_reports()
        tmp = now[1]        # Retrieve the id of the incident report
        cur = retrieve_selected_incident_report(tmp[0])[:-2]
        assert tmp == cur

    def test_delete_incident_report(self):

        now = retrieve_active_incident_reports()
        if not len(now):
            insert_report(
                    name = 'Jia Yun',
                    mobile_number = '+65 12345678',
                    location = 'hall 14',
                    assistance_required = 1,
                    description = 'description',
                    priority_injuries = 1,
                    priority_dangers = 1,
                    priority_help = 1,
                    report_status = 2
            )

        now = retrieve_active_incident_reports()
        assert len(now)

        removed_item = now[0]
        delete_report(now[0][0])

        now = retrieve_active_incident_reports()
        assert removed_item not in now


if __name__ == '__main__':
    __drop_database()
    init_db()

    main()

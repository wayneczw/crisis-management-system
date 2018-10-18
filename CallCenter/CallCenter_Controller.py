# coding: utf-8

from flask import Flask, redirect, render_template, request, session, Blueprint
from CallCenter.CallCenter_Model import *


callcenter_api = Blueprint('callcenter', __name__, template_folder='CallCenter_Views', )
callcenter_api.secret_key = "a2nbs81sSJl8d"  # Set Encryption key to encrypt the Data sent by client during a Session [These Data is stored in the encrypted form]
init_db()  # Initialise database


'''
@app.route() will indicate the web address that we need to type into our Web Browser. 
E.g. For the below, the function "submit_new_incident_report()" will be called whenever the user goes to an Web Address 
that ends with "/submit_new_incident_report"
'''


# First Page of Updating an Incident Report
@callcenter_api.route("/update_incident_report_page", methods = ['GET', 'POST'])
def update_incident_report():
    all_incident_reports = retrieve_all_incident_reports() # Call a Method from Model to retrieve all the Incident Reports
    all_incident_reports.reverse()
    # Render the html page that corresponds to this method [And we give the html file some arguments]:
    return render_template('callcenter_ui_update_incident_report-int.html', columns=['ID', 'First reported time', 'Name', 'Mobile no.' , 'Location', 'Assistance requested', 'Description' , 'Priority on injuries', 'Priority on dangers', 'Priority on help', 'Report status', 'Is first such incident'], items=all_incident_reports)


# Update Information about one particular Incident Report into the DB based on which incident the Call Operator has selected
@callcenter_api.route('/row_detail_for_update/<rowData>', methods = ['GET', 'POST'])
def row_detail_for_update(rowData):


    if request.method == 'POST':  # i.e. Once "Submit" Button is pressed
        id_of_incident_report = request.form['id_of_incident_report'] 
        first_reported = request.form['first_reported']  # Get the "caller_name" from the form that the User has submitted
        first_reported = first_reported + "0000000"   # add back the last 7 digits when we storing the timestamp in database.
        caller_name = request.form['caller_name']  # Get the "caller_name" from the form that the User has submitted
        caller_mobile_number = request.form['caller_mobile_number']
        caller_location = request.form['caller_location']
        type_of_assistance = request.form['type_of_assistance']
        description = request.form['description']
        priority_for_severity_of_injuries = request.form['priority_for_severity_of_injuries']
        priority_for_impending_dangers = request.form['priority_for_impending_dangers']
        priority_for_presence_of_nearby_help = request.form['priority_for_presence_of_nearby_help']
        report_status = request.form['report_status']
        is_first_such_incident = request.form['is_first_such_incident']


        # Update the Report in our Database by calling this method of the Model:
        update_report(id_of_incident_report, caller_name, caller_mobile_number , caller_location, type_of_assistance, description , priority_for_severity_of_injuries, priority_for_impending_dangers, priority_for_presence_of_nearby_help, report_status, is_first_such_incident)


        # Show the Confirmation Page; Note that paramters such as "caller_name" is sent to the html file as an argument.
        # Store some data using Session:
        session['id_of_incident_report'] = id_of_incident_report
        session['first_reported'] = first_reported
        session['caller_name'] = caller_name
        session['caller_mobile_number'] = caller_mobile_number
        session['caller_location'] = caller_location
        session['type_of_assistance'] = type_of_assistance
        session['description'] = description
        session['priority_for_severity_of_injuries'] = priority_for_severity_of_injuries
        session['priority_for_impending_dangers'] = priority_for_impending_dangers
        session['priority_for_presence_of_nearby_help'] = priority_for_presence_of_nearby_help
        session['report_status'] = report_status
        session['is_first_such_incident'] = is_first_such_incident

        # Move to the Confirmation Page now:
        return redirect('/callcenter/incident_report_update_completion_page')
   
    else: # i.e. "Submit" Button has not been pressed

        # Getting an Integer [id_of_incident_report] from the String[rowData]
        id_of_incident_report = ''
        start = True
        for char in rowData:
            if char.isdigit():
                start = False
                id_of_incident_report = id_of_incident_report+char
            else:
                if start == False:
                    break

        # Call a method from the Model to retrieve that Incident Report from DB    
        report = retrieve_selected_incident_report(id_of_incident_report)

        # Break down the incident report that has been retrieved from the DB into dif parts:
        id_of_incident_report = report[0] # get the id of the incident report
        first_reported = report[1]  # timestamp of when the incident is being reported at
        caller_name = report[2]
        caller_mobile_number = report[3]
        caller_location = report[4]
        type_of_assistance = report[5]
        description = report[6]
        priority_for_severity_of_injuries = report[7]
        priority_for_impending_dangers = report[8]
        priority_for_presence_of_nearby_help = report[9]
        report_status = report[10]
        is_first_such_incident = report[11]

        # Render a html file and provide that html file with some arguments           
        return render_template('callcenter_ui_row_detail_for_update.html',
                    id_of_incident_report=id_of_incident_report,
                    first_reported = first_reported,
                    caller_name = caller_name,
                    caller_mobile_number = caller_mobile_number,
                    caller_location = caller_location,
                    description = description,
                    type_of_assistance = type_of_assistance,
                    priority_for_severity_of_injuries = priority_for_severity_of_injuries,
                    priority_for_impending_dangers = priority_for_impending_dangers,
                    priority_for_presence_of_nearby_help = priority_for_presence_of_nearby_help,
                    report_status = report_status,
                    is_first_such_incident = is_first_such_incident
                                )


# Show the Completion Page after Updating an Incident Report
@callcenter_api.route("/incident_report_update_completion_page", methods = ['GET', 'POST'])
def incident_report_update_completion_page():

    
    if request.method == 'POST':  # i.e. "Submit" Button has been pressed
        return redirect('/callcenter/update_incident_report_page')

    # Retrieve Data that has been stored in the Session:
    id_of_incident_report = session['id_of_incident_report'] 
    first_reported = session['first_reported']
    caller_name = session['caller_name']
    caller_mobile_number = session['caller_mobile_number']
    caller_location = session['caller_location']
    type_of_assistance = session['type_of_assistance']
    description = session['description']
    priority_for_severity_of_injuries = session['priority_for_severity_of_injuries']
    priority_for_impending_dangers = session['priority_for_impending_dangers']
    priority_for_presence_of_nearby_help = session['priority_for_presence_of_nearby_help']
    report_status = session['report_status']
    is_first_such_incident = session['is_first_such_incident'] 

    # Some formatting before displaying the data:
    assistance_required_dict = {0:'No Assistance needed', 1:'Emergency Ambulance', 2:'Rescue and Evaluate', 3:'Gas Leak Control'} # a Dict to convert assistance_required from int to string
    report_status_dict = {1:'REPORTED', 2:'PENDING', 3:'CLOSED'} # a Dict to convert report_status required from int to string
    is_first_such_incident_dict = {0:'FALSE', 1:'TRUE'} # a Dict to convert is_first_such_incident from int to string
    first_reported = first_reported[:-7]   # remove last 7 chars [too precise]

    type_of_assistance = assistance_required_dict[int(type_of_assistance)]
    report_status = report_status_dict[int(report_status)]
    is_first_such_incident = is_first_such_incident_dict[int(is_first_such_incident)]  
    
    
    return render_template(
                'callcenter_ui_new_incident_report_update_completion.html',
                id_of_incident_report = id_of_incident_report,
                first_reported = first_reported,
                caller_name = caller_name,
                caller_mobile_number = caller_mobile_number,
                caller_location = caller_location,
                description = description,
                type_of_assistance = type_of_assistance,
                priority_for_severity_of_injuries = priority_for_severity_of_injuries,
                priority_for_impending_dangers = priority_for_impending_dangers,
                priority_for_presence_of_nearby_help = priority_for_presence_of_nearby_help,
                report_status = report_status,
                is_first_such_incident = is_first_such_incident
                            )


# First Page of Deleting an Incident Report
@callcenter_api.route("/delete_incident_report_page", methods = ['GET', 'POST'])
def delete_incident_report():
    all_incident_reports = retrieve_all_incident_reports()
    all_incident_reports.reverse()

    if request.method == 'POST':
        return redirect('/dashboard')
    return render_template('callcenter_ui_delete_incident_report-int.html', columns=['ID', 'First reported time', 'Name', 'Mobile no.' , 'Location', 'Assistance requested', 'Description' , 'Priority on injuries', 'Priority on dangers', 'Priority on help', 'Report status', 'Is first such incident'], items=all_incident_reports)



# Delete Information about one particular Incident Report into the DB based on which incident the Call Operator has selected
@callcenter_api.route('/row_detail_for_delete/<rowData>', methods = ['GET', 'POST'])
def row_detail_for_delete(rowData):


    if request.method == 'POST':
        id_of_incident_report = request.form['id_of_incident_report']
        first_reported = request.form['first_reported']  # Get the "caller_name" from the form that the User has submitted
        first_reported = first_reported + "0000000"   # add back the last 7 digits when we storing the timestamp in database.
        caller_name = request.form['caller_name']  # Get the "caller_name" from the form that the User has submitted
        caller_mobile_number = request.form['caller_mobile_number']
        caller_location = request.form['caller_location']
        type_of_assistance = request.form['type_of_assistance']
        description = request.form['description']
        priority_for_severity_of_injuries = request.form['priority_for_severity_of_injuries']
        priority_for_impending_dangers = request.form['priority_for_impending_dangers']
        priority_for_presence_of_nearby_help = request.form['priority_for_presence_of_nearby_help']
        report_status = request.form['report_status']
        is_first_such_incident = request.form['is_first_such_incident']


        # Delete the Report in our Database by calling this method:
        delete_report(id_of_incident_report)


        # Show the Confirmation Page; Note that paramters such as "caller_name" is sent to the html file as an argument.
        session['id_of_incident_report'] = id_of_incident_report
        session['first_reported'] = first_reported
        session['caller_name'] = caller_name
        session['caller_mobile_number'] = caller_mobile_number
        session['caller_location'] = caller_location
        session['type_of_assistance'] = type_of_assistance
        session['description'] = description
        session['priority_for_severity_of_injuries'] = priority_for_severity_of_injuries
        session['priority_for_impending_dangers'] = priority_for_impending_dangers
        session['priority_for_presence_of_nearby_help'] = priority_for_presence_of_nearby_help
        session['report_status'] = report_status
        session['is_first_such_incident'] = is_first_such_incident

        return redirect('/callcenter/incident_report_delete_completion_page')
        
    else:

        # Getting an Integer ID from the String[rowData]
        id_of_incident_report = ''
        start = True
        for char in rowData:
            if char.isdigit():
                start = False
                id_of_incident_report = id_of_incident_report+char
            else:
                if start == False:
                    break
            
        report = retrieve_selected_incident_report(id_of_incident_report)

        
        id_of_incident_report = report[0] # get the id of the incident report
        first_reported = report[1]  # timestamp of when the incident is being reported at
        caller_name = report[2]
        caller_mobile_number = report[3]
        caller_location = report[4]
        type_of_assistance = report[5]
        description = report[6]
        priority_for_severity_of_injuries = report[7]
        priority_for_impending_dangers = report[8]
        priority_for_presence_of_nearby_help = report[9]
        report_status = report[10]
        is_first_such_incident = report[11]

       
            
        return render_template('callcenter_ui_row_detail_for_delete.html',
                    id_of_incident_report=id_of_incident_report,
                    first_reported = first_reported,
                    caller_name = caller_name,
                    caller_mobile_number = caller_mobile_number,
                    caller_location = caller_location,
                    description = description,
                    type_of_assistance = type_of_assistance,
                    priority_for_severity_of_injuries = priority_for_severity_of_injuries,
                    priority_for_impending_dangers = priority_for_impending_dangers,
                    priority_for_presence_of_nearby_help = priority_for_presence_of_nearby_help,
                    report_status = report_status,
                    is_first_such_incident = is_first_such_incident
                                )



# Show the Completion Page after Deleting an Incident Report
@callcenter_api.route("/incident_report_delete_completion_page", methods = ['GET', 'POST'])
def incident_report_delete_completion_page():


    if request.method == 'POST':
        return redirect('/callcenter/delete_incident_report_page')
    
    id_of_incident_report = session['id_of_incident_report'] 
    first_reported = session['first_reported']
    caller_name = session['caller_name']
    caller_mobile_number = session['caller_mobile_number']
    caller_location = session['caller_location']
    type_of_assistance = session['type_of_assistance']
    description = session['description']
    priority_for_severity_of_injuries = session['priority_for_severity_of_injuries']
    priority_for_impending_dangers = session['priority_for_impending_dangers']
    priority_for_presence_of_nearby_help = session['priority_for_presence_of_nearby_help']
    report_status = session['report_status']
    is_first_such_incident = session['is_first_such_incident'] 

    # Some formatting before displaying the data:
    assistance_required_dict = {0:'No Assistance needed', 1:'Emergency Ambulance', 2:'Rescue and Evaluate', 3:'Gas Leak Control'} # a Dict to convert assistance_required from int to string
    report_status_dict = {1:'REPORTED', 2:'PENDING', 3:'CLOSED'} # a Dict to convert report_status required from int to string
    is_first_such_incident_dict = {0:'FALSE', 1:'TRUE'} # a Dict to convert is_first_such_incident from int to string

    type_of_assistance = assistance_required_dict[int(type_of_assistance)]
    report_status = report_status_dict[int(report_status)]
    is_first_such_incident = is_first_such_incident_dict[int(is_first_such_incident)]  
    first_reported = first_reported[:-7]   # remove last 7 chars [too precise]

    
    return render_template(
                'callcenter_ui_new_incident_report_delete_completion.html',
                id_of_incident_report = id_of_incident_report,
                first_reported = first_reported,
                caller_name = caller_name,
                caller_mobile_number = caller_mobile_number,
                caller_location = caller_location,
                description = description,
                type_of_assistance = type_of_assistance,
                priority_for_severity_of_injuries = priority_for_severity_of_injuries,
                priority_for_impending_dangers = priority_for_impending_dangers,
                priority_for_presence_of_nearby_help = priority_for_presence_of_nearby_help,
                report_status = report_status,
                is_first_such_incident = is_first_such_incident
                            )





# Show the Completion Page after sending an Incident Report
@callcenter_api.route("/incident_report_sent_completion_page", methods = ['GET', 'POST'])
def incident_report_sent_completion_page():

    caller_name = session['caller_name']
    caller_mobile_number = session['caller_mobile_number']
    caller_location = session['caller_location']
    type_of_assistance = session['type_of_assistance']
    description = session['description']
    priority_for_severity_of_injuries = session['priority_for_severity_of_injuries']
    priority_for_impending_dangers = session['priority_for_impending_dangers']
    priority_for_presence_of_nearby_help = session['priority_for_presence_of_nearby_help']
    report_status = session['report_status']


    # Some formatting before displaying the data:
    assistance_required_dict = {0:'No Assistance needed', 1:'Emergency Ambulance', 2:'Rescue and Evaluate', 3:'Gas Leak Control'} # a Dict to convert assistance_required from int to string
    report_status_dict = {1:'REPORTED', 2:'PENDING', 3:'CLOSED'} # a Dict to convert report_status required from int to string
    is_first_such_incident_dict = {0:'FALSE', 1:'TRUE'} # a Dict to convert is_first_such_incident from int to string

    type_of_assistance = assistance_required_dict[int(type_of_assistance)]
    report_status = report_status_dict[int(report_status)]
    

    if request.method == 'POST':
        return redirect('/callcenter/submit_new_incident_report')
    return render_template(
                'callcenter_ui_new_incident_report_sent_completion.html',
                caller_name = caller_name,
                caller_mobile_number = caller_mobile_number,
                caller_location = caller_location,
                description = description,
                type_of_assistance = type_of_assistance,
                priority_for_severity_of_injuries = priority_for_severity_of_injuries,
                priority_for_impending_dangers = priority_for_impending_dangers,
                priority_for_presence_of_nearby_help = priority_for_presence_of_nearby_help,
                report_status = report_status
                            )


@callcenter_api.route("/submit_new_incident_report", methods = ['GET', 'POST'])
def submit_new_incident_report():
    # Public Method
    # To submit a new Incident report into Database; No parameters is required;
    # This Function is called whenever Call Operator need to submit a new Incident Report.

    # If the user has POST sth [i.e. Submitted a form],
    # we will show him/her the "Incident Report has been sent" Confirmation Page.
    if request.method == 'POST':
        caller_name = request.form['caller_name']  # Get the "caller_name" from the form that the User has submitted
        caller_mobile_number = request.form['caller_mobile_number']
        caller_location = request.form['caller_location']
        type_of_assistance = request.form['type_of_assistance']
        description = request.form['description']
        priority_for_severity_of_injuries = request.form['priority_for_severity_of_injuries']
        priority_for_impending_dangers = request.form['priority_for_impending_dangers']
        priority_for_presence_of_nearby_help = request.form['priority_for_presence_of_nearby_help']
        report_status = request.form['report_status']

        # Insert the Report into our Database by calling this method of our Model:
        insert_report(caller_name, caller_mobile_number , caller_location, type_of_assistance, description , priority_for_severity_of_injuries, priority_for_impending_dangers, priority_for_presence_of_nearby_help, report_status)


        # Show the Confirmation Page; Note that paramters such as "caller_name" is sent to the html file as an argument.

        session['caller_name'] = caller_name
        session['caller_mobile_number'] = caller_mobile_number
        session['caller_location'] = caller_location
        session['type_of_assistance'] = type_of_assistance
        session['description'] = description
        session['priority_for_severity_of_injuries'] = priority_for_severity_of_injuries
        session['priority_for_impending_dangers'] = priority_for_impending_dangers
        session['priority_for_presence_of_nearby_help'] = priority_for_presence_of_nearby_help
        session['report_status'] = report_status

        return redirect('/callcenter/incident_report_sent_completion_page')

    # If User has not sent anything, we will show him/her the Form to submit a New Incident Report.
    return render_template('callcenter_ui_new_incident_report_submission-int.html')




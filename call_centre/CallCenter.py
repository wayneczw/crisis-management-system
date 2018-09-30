# coding: utf-8

from flask import Flask, redirect, render_template, request


app = Flask(__name__, template_folder = "templates")


@app.route("/", methods = ['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        return redirect('/submit_new_incident_report')
    return render_template('callcenter_ui_main.html')

# If User has not sent anything, we will show him/her the Form to submit a New Incident Report.


'''
@app.route() will indicate the web address that we need to type into our Web Browser. 
E.g. For the below, the function "submit_new_incident_report()" will be called whenver the user goes to an Web Address 
that ends with "/submit_new_incident_report"
'''


@app.route("/submit_new_incident_report", methods = ['GET', 'POST'])
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

        return render_template(
                'callcenter_ui_new_incident_report_sent_completion.html',
                caller_name = caller_name,
                caller_mobile_number = caller_mobile_number,
                caller_location = caller_location,
                description = description,
                type_of_assistance = type_of_assistance,
                priority_for_severity_of_injuries = priority_for_severity_of_injuries,
                priority_for_impending_dangers = priority_for_impending_dangers,
                priority_for_presence_of_nearby_help = priority_for_presence_of_nearby_help
        )
    # Show the Confirmation Page; Note that caller_name is sent to the html file as an argument.

    return render_template('callcenter_ui_new_incident_report_submission.html')

# If User has not sent anything, we will show him/her the Form to submit a New Incident Report.


if __name__ == "__main__":
    app.run()  # app is an instance of the 'Flask' - see the first few lines.

'''
Public Method
To modify an existing Incident Report that has been stored into Database; 
No parameters is required; This Function is called whenever Call Operator need to modify an Existing Incident Report.
'''


def modify_incident_report():
    pass


'''
Public Method
To delete an existing Incident Report that has been stored into Database; 
No parameters is required; This Function is called whenever Call Operator need to delete an Existing Incident Report.
'''


def delete_incident_report():
    pass


'''
Private Method
To verify if a newly submitted Incident Report pertains to an Incident 
which has already been reported or has never been reported before;

Parameters required are caller_location							str
						type_of_assistance						enum
						priority_for_severity_of_injuries		int
						priority_for_impending_dangers			int
						priority_for_presence_of_nearby_help	int
						
This Function is called by the Function "submit_new_incident_report()".
Returns a Boolean - True if Incident has not been reported before; 
					False if Incident has already been reported before
'''


def __verify_incident_report(caller_location, type_of_assistance, priority_for_severity_of_injuries,
                             priority_for_impending_dangers,
                             priority_for_presence_of_nearby_help):
    pass


'''
Private Method
To allocate an overall Priority number to the Incident Reported.

Parameters required are priority_for_severity_of_injuries		int
						priority_for_impending_dangers			int
						priority_for_presence_of_nearby_help	int

This Function may be called by the Function "submit_new_incident_report()".
'''


def __priority_allocation(priority_for_severity_of_injuries, priority_for_impending_dangers,
                          priority_for_presence_of_nearby_help):
    pass


'''
Private Method
To send a SMS to SCDF or Singapore Power to ask for their assistance for a distressed Member of Public.

Parameters required are caller_name								str
						caller_mobile_number					str
						caller_location							str
						type_of_assistance						enum
						description								str
						priority_for_severity_of_injuries		int
						priority_for_impending_dangers			int
						priority_for_presence_of_nearby_help	int

This Function is called by the Function "submit_new_incident_report()".
'''


def __send_sms(caller_name, caller_mobile_number, caller_location, type_of_assistance, description,
               priority_for_severity_of_injuries, priority_for_impending_dangers,
               priority_for_presence_of_nearby_help):
    pass



"""
To install:
pip3 install locustio

To run load test:

1) first, run the main app [get the system running first]

2) in a separate terminal: ["localhost" below refers to where you are running the main app/our system]
locust -f load_test_locust.py --host=http://localhost     

3) Then, in a separate web browser tab [will take you to the locust web interface]:
go to http://127.0.0.1:8089/

4) Set the number of users, and hatch rate

5) Look at the statistics - No "# fails" means that our system is coping well.

To run performance test:

1) first, run the main app [get the system running first]

2) in a separate terminal: ["localhost" below refers to where you are running the main app/our system]
locust -f load_test_locust.py --no-web -c 1 -r 1 -t 60s --host=http://localhost

3) Then, wait for the command to complete and at the end there is a log on the performance for the response time
for each test case
"""






from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):





    # First method that is called
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    # Doing load test on the login function of our system
    def login(self):
        res = self.client.post("/login", {"username":"government_agency_test", "password":"government_agency_test", "role":"Government Agency"})
        if "Invalid Credentials" in res.text:
            print("Incorrect Username or Password or Role") # But the system is still functioning fine because the Locust has not detected a failure such as overwhelming traffic
        else:
            print("Valid Credentials inputted")


    # Doing load test on the dashboard page of our system
    @task(1)
    def dashboard_load_test(self):
        self.client.get("/dashboard")


    # Doing load test on the Weather Map page of our system
    @task(2)
    def weather_map_load_test(self):
        self.client.get("/map/weather")


    # Doing load test on the Call Center page of our system
    @task(3)
    def call_center_load_test(self):
        # The update page
        self.client.get("/callcenter/update_incident_report_page")

        # submit new incident page
        self.client.get("/callcenter/submit_new_incident_report")
        res = self.client.post("/callcenter/submit_new_incident_report", {"caller_name":"Peter Henderson", "caller_mobile_number":"91234567", "caller_location":"Pioneer Mrt Station", "type_of_assistance":"2", "description":"I didn't see anything","priority_for_severity_of_injuries":"2", "priority_for_impending_dangers":"3","priority_for_presence_of_nearby_help":"4", "report_status":"2" })
        if "successfully submitted" in res.text:
            print("Incident Report successfully submitted")
        else:
            print("Unsuccessful Incident Report submission")
   


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 3000

## Crisis Management System - Giligili

Updated: 14.10.2018 by HaoHao

## Setup steps:

- Install dependencies via:
```
pip install -r requirements.txt
``` 
- Delete `app.db` and `database.db` in root folder if there is any.
- Initialize database:
```
python db_test.py
```
- Run the main application:
```
python app.py
``` 
- Open `localhost:5000` in your browser to view the login page. And enjoy!


### About login 
The file `db_test.py` creates dummy accounts for login. 
You can use either one of the following to login
(Username, Password, Role):
```bibtex
admin_test              admin_test              Admin
call_operator_test      call_operator_test      Call Operator
government_agency_test  government_agency_test  Government Agency
```

Access control feature has yet to be done, so for the dashboard looks
the same for all types of user roles.

After successful login, you will be redirected to the dashboard route at `localhost:5000/dashboard`.

### About file organization
For each subsystem, the file structure is organized as below:
```
Subsystem-Name
    -- templates
    -- static (if any)
    -- subsystem-logic-controller.py
```
Only `app.py` and its dependencies lie at the root directory.

Minimum code changes are made for docking each subsystem in.
Often, the changes are (i) change Flask app into Blueprint and register to main app;
(ii) extend dashboard-base.html to each .html template file.



## Crisis Management System - Giligili

Updated: 2.10.2018 by HaoHao

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

## Setup steps:

- Install dependencies via:
```
pip install -r requirements.txt
``` 
- Run login.py to start the server
```
python app.py
``` 
- Open `localhost:5000` in your browser to view the login page.


### About login 
All accounts created are stored in `db/userlist.csv`. Please
refer to the file if you need to use dummy accounts for testing. 

After successful login, you will be redirected to the dashboard route at `localhost:5000/dashboard`.


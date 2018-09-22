## CMS Dashboard

Setup steps:

- Install dependencies via:
```
pip install -r requirements.txt
``` 
- Run login.py to start the server
```
python login.py
``` 
- Open `localhost:5000/login` in your browser to view the login page.


### About login 
All accounts created are stored in `db/userlist.csv`. Please
refer to the file if you need to use dummy accounts for testing. 

After successful login, you will be redirected to the dashboard route at `localhost:5000/dashboard`.


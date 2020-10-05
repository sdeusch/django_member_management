
# Member Data Management with Django

This an application in Python and Django which serves an API to fetch and create members. 
The CSV file is provided with the following columns:

* ID
* First Name
* Last Name
* Phone Number
* Client Member ID
* Account ID

These rows of the file represented the data for a member.
The app allows to 
* Get a member for a given Account ID
* Get a member by their ID
* Get a member by their Phone Number
* Get a member by their Client Member ID
* Batch insert members by uploading a CSV (similar to the one provided)


### Installation
```bash
git clone git@github.com:sdeusch/django_member_management.git 
```
On a Python 3.6+ environment create virtual environmnt and activate it
```bash
python3 -m venv venv
source venv/bin/activate
```

Run pip to install the Django framework and dependencies:
```bash
pip install -r requirements.txt
```

Change into directory Website where the Django application is
```bash
cd Website/
```

Create Admin Superuser, specifiying a username, email, and a password. 
```bash
 python manage.py createsuperuser 
```

Create the migrations
```bash
python manage.py makemigrations
```

Apply the migrations
```bash
python manage.py migrate
```

Start the web server
```bash
python manage.py runserver
```

You should see 
```bash
Starting development server at http://127.0.0.1:8000/
```
Success!


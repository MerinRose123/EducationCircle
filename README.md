# EducationCircle

The project is aimed to created a platform for the preparation of various exams. It includes mock tests, previous year questions, quiz as well as a community to ask doubts and all.

The database used is SQLLIte which is inbuild in Django. So no need to install it separately.
Database : SQLite

### Dependencies

Python = `Python 3.6.9`

### Running in local

#### Virtual environment Creation (Optional)
Create a virtual environment in which the dependencies should be installed. Run the following commands in terminal 
1. `pip install virtualenv`
2. `virtualenv eduenv`
3. `source eduenv/bin/activate`

#### Initializing and Running the application
Type the following commands in the terminal where the project is situated.( EducationCircle)
1. `cd EduCircleBackend`
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py runserver`
5. Load the default fixtures which will add default categories, exam types as well as sample questions.
`chmod +x populate_data.sh`
`./populate_data.sh`

### Ruuning in Production
The app is deployed in heroku. After any code change follow the steps
1. `git add -A` to add all changes
2. `git commit` to commit the changes
3. `git push heroku master` to deploy the code to heroku.



# Event Email Scheduler
### Tech Used
- Python
- Django
- DjangoORM
- Celery
- CeleryBeat
- Redis
### Features

- Loads sample data automatically using "Load data from Sample data Set" url.
- See various tables data at home page using various urls.
- Once the project and scheduler is up and running, it will send automatic emails to employee's on their special ocassions on a different thread using multithreading which is implemented using Celery.
- Logs are created in Event Log and System Log tables.


#### How to deploy the project on local?
1. Install python, celery, celery-beat, redis on Windows, linux machine.
2. Git clone the repo at the desired folder.
3. Go to folder "event_checker" and Use the requirements.txt file to install the python dependant libraries. using the command "pip install requirements.txt".
4. Go to file "event_checker\settings.py" and add "EMAIL_HOST_USER = '' " and "EMAIL_HOST_PASSWORD = ''" - This email user and email password will be used to send the emails. 
5. Open the terminal run "celery -A event_checker.celery worker --pool=solo -l info" -> this will run the celery worker.
6. In a new terminal run "celery -A event_checker.celery beat -l info" -> this will run the celery beat.
7. Now run the command "python manage.py runserver" -> this will start our event checker scheduler program with email sender to go live at 12:01 AM everyday. You can change this time by going to file "event_checker\celery.py" look for "schedule: crontab()" and give the cron time of your choice.
8. Next step would be to tease the setup, for that we have to load data with sample employee today's event data which can be done by creating the superuser account using the command "python3 manage.py createsuperuser", input the required values.
9. Now go to url "http://127.0.0.1:8000/admin/" -> Login using the superuser credentials,To add data.
10. You can also add data to dataset folder to respective csv's in the repo and then load the dataset to our database which can be done by going to url "http://127.0.0.1:8000/" and clicking "Load data from Sample data Set".
11. Now our event email sender is live.
12. And table data can be viewed at this url "http://127.0.0.1:8000/" -> Select the required table to view their data.

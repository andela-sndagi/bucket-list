from app import app
from flask.ext.script import Manager, prompt_bool
from app.models import initialise, drop

app.config.from_object('config.DevelopmentConfig')

# Setup manager to allow runserver, shell and migrate at runtime
manager = Manager(app)


# Add two commands 'start' and 'stop'
@manager.command
def start():
    """Start Application by creating Database and tables within."""
    print "Bucket-list API is initializing... \n(If it is your first \
    RUN you will have demo data according to the TASK segment in the README)\n \
    (If you want to do away with previous data and start)\n \
    RUN 'python api/manage.py exit' after-which you\n \
    RUN 'python api/manage.py start' \n \
    Otherwise proceed to run the app 'python api/manage.py runserver'"
    initialise()

@manager.command
def stop():
    """Exit application by deleting Database and its contents."""
    if prompt_bool(
    "Bucket-list API is exiting...\n\
    Are you sure you want to exit and lose all your data?\n\
        Type 'Y/y' - YES\n\
        Type 'N/n' - NO"):
        drop()

manager.run()

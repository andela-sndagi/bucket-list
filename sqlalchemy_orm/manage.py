# sqlalchemy_orm/api.py

from app import app
from sqlalchemy_orm.models import initialise, drop

from flask.ext.script import Manager, prompt_bool

# Setup manager to allow runserver, shell and migrate at runtime
manager = Manager(app)

@manager.command
def start():
    """Start Application by creating Database and tables within."""
    print "Bucketlist API is initialising... \n(If it is your first RUN you will have demo data according to the TASK segment in the README)\n  (If you want to do away with previous data and start)\n     RUN 'python api.py exit' afterwhich you\n     RUN 'python api.py start' \n  Otherwise proceed to run the app 'python api.py runserver'"
    initialise()


@manager.command
def exit():
    """Exit application by deleting Database and its contents."""
    if prompt_bool(
    "Bucketlist API is exitting...\n\
    Are you sure you want to exit and lose all your data?\n\
        Type 'Y/y' - YES\n\
        Type 'N/n' - NO"):
        drop()

manager.run()

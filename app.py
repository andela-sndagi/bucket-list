import os, sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import Flask, render_template, request, redirect, url_for
from models import *

app = Flask(__name__)

@app.before_request
def before_request():
    # create db if needed and connet
    initialize_db()

@app.teardown_request
def teardown_request(exception):
    # close the db connection
    db.close()

@app.route('/')
def home():
    # render the home page with the saved Bucketlists
    return render_template('home.html', bucketlists=Bucketlist.select().order_by(Bucketlist.date_created.desc()))

@app.route('/new_bucketlist/')
def new_bucketlist():
    return render_template('new_bucketlist.html')

@app.route('/create/', methods=['POST'])
def create_bucketlist():
    # create the new Bucketlist
    Bucketlist.create(
        name = request.form['title'],
        created_by = request.form['text']
    )

    # return the user to the home page
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
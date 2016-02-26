from flask import Flask

from models import initialize_db, db

app = Flask(__name__)  # Initialise Flask


@app.before_request
def before_request():
    """create db if needed and connect"""
    initialize_db()


@app.teardown_request
def teardown_request(exception):
    """Close the db connection"""
    db.close()

@app.route('/', methods=(['GET']))
def api_index():
    """Welcome note at index"""
    return "Bucket List Service API is ready"

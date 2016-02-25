from flask import Flask

app = Flask(__name__)  # Initialise Flask


@app.route('/', methods=(['GET']))
def api_index():
    """Welcome note at index"""
    return "Bucket List Service API is ready"

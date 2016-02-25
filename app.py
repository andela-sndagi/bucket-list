from flask import Flask

app = Flask(__name__)  # Initialise Flask


"""Welcome note"""
@app.route('/', methods=(['GET']))
def api_index():
    return "Bucket List Service API is ready"

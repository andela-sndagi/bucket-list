import datetime
import re  # We'll need this for email pattern match
import json
from flask import Flask, jsonify, request, abort, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth  # We'll need this for auth
from flask_peewee.utils import get_object_or_404
from models import *

app = Flask(__name__)  # Initialise Flask

@app.before_request
def before_request():
    # create db if needed and connect
    initialize_db()

@app.teardown_request
def teardown_request(exception):
    # close the db connection
    db.close()


"""
Bucket List Collection [/bucketlists/]
"""
@app.route('/bucketlists/', methods = (['GET']))
def get_bucketlists():
    # bucketlist = {bucket_lists=[bucketlists={}]}
    bucketlists = []
    for bucketlist in Bucketlist.select():
        bucketlists.append({'id': bucketlist.id,
                            'name': bucketlist.name,
                            'Created on':
                            bucketlist.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                            'Recently updated on':
                            bucketlist.date_modified.strftime("%Y-%m-%d %H:%M:%S")})
    return jsonify({'List of bucketlists': bucketlists})

@app.route('/bucketlists/', methods = (['POST']))
def create_bucketlist():
    # The Json accepted
    # {
    #     "name": "Travel", (unique bucketlist name)
    #     "created_by": "creator"
    # }
    if not request.json or not 'name' in request.json:
        abort(400)
    name = request.json['name']
    created_by = request.json['created_by']
    parameters = request.json
    bucketlist = Bucketlist(**parameters)
    bucketlist.save()

    return jsonify({'bucketlist created': bucketlist.name}), 201


"""
Single Bucketlist [/bucketlists/<id>]
"""
@app.route('/bucketlists/<int:bucketlist_id>/', methods=(['GET']))
def get_single_bucketlist(bucketlist_id):
    bucketlist = Bucketlist.get(Bucketlist.id == bucketlist_id)
    return jsonify({'id': bucketlist.id,
                    'name': bucketlist.name,
                    'items': len(bucketlist.items),
                    'Bucketlist created on':
                    bucketlist.date_created.strftime("%Y-%m-%d %H:%M:%S"),
                    'Bucketlist updated on':
                    bucketlist.date_modified.strftime("%Y-%m-%d %H:%M:%S")})

@app.route('/bucketlists/<int:bucketlist_id>/', methods=(['PUT']))
def update_bucketlist(bucketlist_id):
    bucketlist = Bucketlist.get(Bucketlist.id == bucketlist_id)
    # The Json accepted
    # {
    # "name": "Stan"
    # }
    bucketlist.name = request.json['name']
    bucketlist.date_modified = datetime.datetime.now()
    # Change modified time to NOW
    bucketlist.save()
    return jsonify({'id': bucketlist.id,
                    'name': bucketlist.name,
                    'Bucketlist created on': bucketlist.date_created,
                    'Bucketlist updated on': bucketlist.date_modified})

@app.route('/bucketlists/<int:bucketlist_id>/', methods=(['DELETE']))
def delete_bucketlist(bucketlist_id):
    bucketlist = Bucketlist.get(Bucketlist.id == bucketlist_id)
    bucketlist.delete_instance()
    return jsonify({'Bucketlist deleted': bucketlist.name}), 204


"""
Items in a Bucketlist [/bucketlists/<id>/items/]
"""
@app.route('/bucketlists/<int:bucketlist_id>/items/', methods=['POST'])
def create_blitem(bucketlist_id):
    name = request.json['name']
    done = request.json['done']
    parameters = request.json
    item = BucketlistItem(**parameters)
    bucketlist = Bucketlist.get(Bucketlist.id == bucketlist_id)
    item.bucketlist = bucketlist
    item.save()
    return jsonify({'Item created': item.name})


"""
Single Item in a Bucketlist [/bucketlists/<id>/items/<item_id>]
"""
@app.route('/bucketlists/<int:bucketlist_id>/items/<int:item_id>/', methods = (['PUT']))
def update_blitem(bucketlist_id, item_id):
    # The Json accepted
    # {
    #     "name": "I need to do Y",
    #     "done": True
    # }
    bucketlist = Bucketlist.get(Bucketlist.id == bucketlist_id)
    item = BucketlistItem.get(BucketlistItem.id == item_id)
    item.name = request.json['name']
    item.done = request.json['done']
    item.date_modified = datetime.datetime.now()
    # Change modified time to NOW
    item.save()
    return jsonify({'id': item.id,
                    'name': item.name,
                    'in bucketlist': bucketlist.name,
                    'Bucketlist created on': item.date_created,
                    'Bucketlist updated on': item.date_modified})

@app.route('/bucketlists/<int:bucketlist_id>/items/<int:item_id>/', methods = ['DELETE'])
def delete_blitem(bucketlist_id, item_id):
    item = BucketlistItem.get(BucketlistItem.id == item_id)
    item.delete_instance()
    return jsonify({'Bucketlist deleted': item.name}), 204

if __name__ == '__main__':
    app.run(debug=True)

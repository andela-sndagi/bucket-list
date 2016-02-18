import re  # We'll need this for email pattern match
from flask import Flask, jsonify, request, abort, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth  # We'll need this for auth
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
        bucketlists.append({'id':bucketlist.id, 'name':bucketlist.name})
    return jsonify({'bucketlists': bucketlists})

@app.route('/bucketlists/', methods = (['POST']))
def create_bucketlist():
    # The Json accepted
    # {
    #     "name": "Freb",
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
@app.route('/bucketlists/<int:id>', methods = (['GET']))
def get_single_bucketlist(id):
    bucketlistitems = []
    for bucketlistitem in BucketlistItem.select():
        bucketlistitems.append({'id':bucketlistitem.id, 'name':bucketlistitem.name, 'done':bucketlistitem.done })
    return jsonify({'items': bucketlistitems})

@app.route('/bucketlists/<int:id>', methods = (['PUT']))
def update_bucketlist(id):
    item = [item for item in items if item['id'] == id]
    # The Json accepted
    # {
    # "name": "Stan",
    # "date_modified": "2015-08-12 11:59:23",
    # "done": null
    # }
    item[0]['name'] = request.json['name']
    item[0]['date_modified'] = request.json['date_modified']
    item[0]['done'] = request.json['done']
    return jsonify({'item': item[0]})

@app.route('/bucketlists/<int:id>', methods = (['DELETE']))
def delete_bucketlist(id):
    item = [item for item in items if item['id'] == id]
    if len(item) == 0:
        abort(404)
    items.remove(item[0])
    return jsonify({'result': True})

"""
Items in a Bucketlist [/bucketlists/<id>/items/]
"""
@app.route('/bucketlists/<int:id>/items', methods = ['POST'])
def get_blitem(id):
    # bl_id = self.id
    name = request.json['name']
    done = request.json['done']
    created_by = request.json['created_by']
    parameters = request.json
    item = BucketlistItem(**parameters)
    item.save()
    return jsonify({'item': item.name})


"""
Single Item in a Bucketlist [/bucketlists/<id>/items/<item_id>]
"""
@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods = (['PUT']))
def update_blitem(id, item_id):
    item = [item for item in items if item['id'] == id]
    # The Json accepted
    # item = {
    #     'id': 2,
    #     "item_id": items[-1]['id'] + 1,
    #     "name": "I need to do Y",
    #     "date_created": "2015-08-12 11:59:23",
    #     "date_modified": "2015-08-12 11:59:23",
    #     "done": True
    # }
    item[0]['name'] = request.json['name']
    item[0]['date_modified'] = request.json['date_modified']
    item[0]['done'] = request.json['done']
    return jsonify({'item': item[0]})

@app.route('/bucketlists/<int:id>/items/<int:item_id>', methods = ['DELETE'])
def delete_blitem(id, item_id):
    pass

if __name__ == '__main__':
    app.run(debug=True)

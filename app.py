from flask import Flask, jsonify, request, abort
from models import *


app = Flask(__name__) # Initialise Flask

@app.before_request
def before_request():
    # create db if needed and connect
    initialize_db()

@app.teardown_request
def teardown_request(exception):
    # close the db connection
    db.close()

# @app.route('/auth/login', methods = ['POST'])
# def login():
#     token = [
#         {
#             "token": "t0k3n"
#         }
#     ]
#     return jsonify({'token': token})

# @app.route('/auth/register', methods = ['POST'])
# def register():
#     return 'POST'

"""
Bucket List Collection [/bucketlists/]
"""

bucketlists = [
    {
        "id": 1,
        "name": "BucketList1",
    },
    {
        "id": 2,
        "name": "BucketList2",
    },
    {
        "id": 3,
        "name": "BucketList3",
    }
]

@app.route('/bucketlists', methods = (['GET']))
def get_bucketlists():
    return jsonify({'bucketlists': bucketlists})

@app.route('/bucketlists', methods = (['POST']))
def create_bucketlist():
    # bucketlist = Bucketlist.create(name = request.json['name'])
    # bucketlist.save()
    # return jsonify({'bucketlist': bucketlist}), 201
    if not request.json or not 'name' in request.json:
        abort(400)
    bucketlist = {
        'id': bucketlists[-1]['id'] + 1,
        'name': request.json['name'],
    }
    bucketlists.append(bucketlist)
    return jsonify({'bucketlist': bucketlist}), 201

"""
Single Bucketlist [/bucketlists/<id>]
"""

items = [
    {
        "id": 1,
        "name": "I need to do X",
        "date_created": "2015-08-12 11:57:23",
        "date_modified": "2015-08-12 11:57:23",
        "done": False
    }
]

@app.route('/bucketlists/<id>', methods = (['GET']))
def get_single_bucketlist(id):
    return jsonify({'items': items})


@app.route('/bucketlists/<int:id>', methods = (['PUT']))
def update_bucketlist(id):
    item = [item for item in items if item['id'] == id]
    # if len(item) == 0:
    #     abort(404)
    # if not request.json:
    #     abort(400)
    # if 'name' in request.json and type(request.json['name']) != unicode:
    #     abort(400)
    # if 'date_modified' in request.json and type(request.json['date_modified']) is not unicode:
    #     abort(400)
    # if 'done' in request.json and type(request.json['done']) is not bool:
    #     abort(400)
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

# def get_task(task_id):
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': task[0]})

# def specificbl(id):
#     if request.method == 'GET':
#         return jsonify({'items': items})
#     elif request.method == 'PUT':
#         item = [item for item in items if item['id'] == item_id]
#         if len(item) == 0:
#             abort(404)
#         if not request.json:
#             abort(400)
#         if 'name' in request.json and type(request.json['name']) != unicode:
#             abort(400)
#         if 'date_modified' in request.json and type(request.json['date_modified']) is not unicode:
#             abort(400)
#         if 'done' in request.json and type(request.json['done']) is not bool:
#             abort(400)
#         item[0]['name'] = request.json.get('name', item[0]['name'])
#         item[0]['date_modified'] = request.json.get('date_modified', task[0]['date_modified'])
#         item[0]['done'] = request.json.get('done', item[0]['done'])
#         return jsonify({'item': item[0]})
#     elif request.method == 'DELETE':
#         task = [item for item in items if item['id'] == item_id]
#         if len(item) == 0:
#             abort(404)
#         items.remove(item[0])
#         return jsonify({'result': True})



# Single Item in a Bucketlist [/bucketlists/<id>/items/<item_id>]

@app.route('/bucketlists/<id>/items/', methods = ['POST'])
def blitems(id):
    if not request.json or not 'title' in request.json:
        abort(400)
        item = {
            "item_id": 2,
            "name": "I need to do Y",
            "date_created": "2015-08-12 11:59:23",
            "date_modified": "2015-08-12 11:59:23",
            "done": True
        }
        items.append(item)
        return jsonify({'item': item}), 201

# @app.route('/bucketlists/<id>/items/<item_id>', methods = (['PUT'], ['DELETE']))
# def bliitem(id, item_id):
#     pass

if __name__ == '__main__':
    app.run(debug=True)

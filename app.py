from flask import Flask, jsonify, request, abort, session, escape
import re
from models import *


app = Flask(__name__) # Initialise Flask
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

@app.before_request
def before_request():
    # create db if needed and connect
    initialize_db()

@app.teardown_request
def teardown_request(exception):
    # close the db connection
    db.close()


"""
User Authentification [/auth/login/]
"""
@app.route('/auth/login/', methods = ['POST'])
def login():
    # Json accepted
    # {
    #     "username": "us3rn@m3",
    #     "password": "p@ssw0rd"
    # }
    username = request.json['username']
    password = request.json['password']

    # Abort if the fields entered are not username and/or password
    if not username and not password:
        abort(400)

    # Create session
    session['username'] = username
    # return 'Logged in as %s' % escape(session['username'])
    # return app.get_secret_key()

    # Get the user with that username
    user = User.get(User.username == username)
    # jwt.encode(user, 'secret', algorithm='HS256')
    # error = None
    # Confirm if the password is the same as the registered one
    if user.valid_password(password):
        user_token = user.log_the_user_in()
        return jsonify({'token': user_token.encode('hex')})
    else:
        error = 'Invalid username/password'
        return jsonify({'error': error})

@app.route('/auth/logout/', methods = ['POST'])
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return jsonify({'message': 'You are logged out'})



"""
User Registration [/auth/register/]
"""
@app.route('/auth/register/', methods=['POST'])
def register():
    # Json accepted in this route
    # {
    #     "username": "us3rn@m3",
    #     "email": "email@user.com",
    #     "password": "p@ssw0rd",
    #     "confirm_password": "p@ssw0rd"
    # }
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    confirm_password = request.json['confirm_password']
    del request.json['confirm_password']
    parameters = request.json

    user = User(**parameters)
    # return user.username
    if not user.username and not user.password:
        abort(400)
    # Confirm password
    if user.password != confirm_password:
        abort(400)
    # Validate email
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    if pattern.match(user.email) is None:
        abort(400)
    user.save()
    return jsonify({'message': 'Successful registration'}), 201


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
items = [
    {
        "id": 1,
        "bl_id": 1,
        "name": "I need to do X",
        "date_created": "2015-08-12 11:57:23",
        "date_modified": "2015-08-12 11:57:23",
        "done": False
    }
]

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

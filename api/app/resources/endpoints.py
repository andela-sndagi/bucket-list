import datetime

from flask import g
from flask_restful import Resource, fields, marshal_with, reqparse

from ..models import db, Bucketlist, BucketlistItem, User
from bucketlist_items import bucketlist_items_fields

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.login_required

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


bucketlist_items_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'bucketlist': fields.Integer,
    'date_created': fields.String,
    'date_modified': fields.String,
    'done': fields.Boolean,
}

bucketlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'items': fields.Nested(bucketlist_items_fields),
    'created_by': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
}


class Bucketlists(Resource):
    """
    Bucket List Collection [/bucketlists/]
    """

    def __init__(self):
        """Instantiate route request parameters"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str,
                                 help='Enter name of Bucketlist', location='json')
        self.parser.add_argument('created_by', type=str,
                                 help="Creator of the bucketlist",
                                 location='json')
        super(Bucketlists, self).__init__()

    @auth.login_required
    @marshal_with(bucketlist_fields)
    def get(self):
        """GET endpoint"""
        bucketlists = []
        # Bucketlist.query.all() returns a query that has to be iterated through
        for bucketlist in Bucketlist.query.all():
            bucketlists.append(bucketlist)
        return bucketlists

    @auth.login_required
    def post(self):
        """POST endpoint"""
        args = self.parser.parse_args()
        name = args['name']
        created_by = args['created_by']
        new_bucket_list = Bucketlist(name=name, created_by=created_by)
        name = new_bucket_list.name
        db.session.add(new_bucket_list)
        db.session.commit()
        return {'message': "'{}' successfully created".format(name)}, 201


class SingleBucketlist(Resource):
    """
    A Single Bucketlist [/bucketlists/<>]
    """

    def __init__(self):
        """Instantiate route request parameters"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str,
                                 help='Enter name of Bucketlist',
                                 location='json')
        super(SingleBucketlist, self).__init__()

    @auth.login_required
    @marshal_with(bucketlist_fields)
    def get(self, id):
        """GET endpoint"""
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        return bucketlist

    @auth.login_required
    def put(self, id):
        """PUT endpoint"""
        args = self.parser.parse_args()
        name = args['name']
        bucket_list = Bucketlist.query.filter_by(id=id).first()
        bucket_list.name = name
        bucket_list.date_modified = datetime.datetime.now(
            ).replace(microsecond=0)
        db.session.commit()
        return {'message': "Bucketlist #{} Successfully updated".format(
            bucket_list.id)}, 200

    @auth.login_required
    def delete(self, id):
        """DELETE endpoint"""
        bucket_list = Bucketlist.query.filter_by(id=id).one()
        db.session.delete(bucket_list)
        db.session.commit()
        # print to console
        print "BucketlistItem entitled '{}' Successfully deleted".format(
            bucket_list.name)
        return {}, 204


class BucketlistItems(Resource):
    """
    Bucketlist items
    [/bucketlists/<list_id>/items/]
    """

    def __init__(self):
        """Instantiate route request parameters"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str,
                                 help='Enter item title', location='json')
        super(BucketlistItems, self).__init__()

    @auth.login_required
    def post(self, id):
        """post on the url"""
        args = self.parser.parse_args()
        title = args['title']
        new_bucket_list_item = BucketlistItem(title=title, bucketlist=id)
        title = new_bucket_list_item.title
        db.session.add(new_bucket_list_item)
        db.session.commit()
        return {'message': "Item '{0}' successfully created in Bucketlist #{1}".format(title, id)}, 201


class SingleBucketlistItem(Resource):
    """
    Bucketlist items
    [/bucketlists/<id>/items/<item_id>]
    """

    def __init__(self):
        """Instantiate route request parameters"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str,
                                 help='Enter item title', location='json')
        self.parser.add_argument('done', type=bool,
                                 help="Change to 'true' if item is done",
                                 location='json')
        super(SingleBucketlistItem, self).__init__()

    @auth.login_required
    def put(self, id, item_id):
        """PUT endpoint"""

        bucket_list_item = BucketlistItem.query.filter_by(
            bucketlist=id).all()[item_id-1]

        args = self.parser.parse_args()
        title = args['title']
        done = args['done']
        bucket_list_item.title = title
        bucket_list_item.date_modified = datetime.datetime.now().\
            replace(microsecond=0)
        bucket_list_item.done = done
        db.session.commit()
        return {"message": "BucketlistItem {0} Successfully updated".
                format(bucket_list_item.id)}, 200

    @auth.login_required
    def delete(self, id, item_id):
        """DELETE endpoint"""

        bucket_list_item = BucketlistItem.query.filter_by(
            bucketlist=id).all()[item_id-1]

        db.session.delete(bucket_list_item)
        db.session.commit()

        # printed on console
        print "BucketlistItem entitled {} Successfully deleted".format(
            bucket_list_item.title)
        return {}, 204

import datetime

from flask import g, request
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.paginate import Pagination

from flask_restful import Resource, fields, marshal_with, reqparse, marshal

from ..models import db, Bucketlist, BucketlistItem, User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
    # get the token from the header
    token = request.headers.get('token')

    # Authenticate by token
    user = User.verify_auth_token(token)
    if not user:
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

class Limit(object):
    """
    This class's attribute helps maintains the limit (content per page limit)
    across separate client page requests.
    """
    limit = 20

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
    def get(self, page=1):
        """GET endpoint"""
        bucketlists = []

        try:
            # Get the limit specified by the client
            limit = int(request.args.get('limit', 0))
        except ValueError:
            # If limit specified by client isn't number type, ignore
            # that and default to 20
            limit = 20

        if limit:
            # if limit is greater than maximum, default to 100
            if limit > 100:
                Limit.limit = 100
            elif limit < 1:
            # if limit is <= 0, default to 20
                Limit.limit = 20
            else:
                Limit.limit = limit

        current_user = User.verify_auth_token(request.headers.get('token'))

        # the "search bucketlist by name" parameter
        search = False
        qs = request.args.get('q')
        if qs:
            search = True
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1

        if search:
            query = Bucketlist.query.filter_by(
                name=qs)
            if query.count() == 0:
                return {"message": "No search results"}
            else:
                info = {"message": "Search results"}
                return [info, marshal(query.first(), bucketlist_fields)]

        bucketlists = Bucketlist.query.all()
        pagination = Pagination(per_page=Limit.limit, page=page,
                                total=len(bucketlists), search=search,
                                record_name='bucketlists')
        info = {"Pagination Details": {
            "results": pagination.endpoint,
            "per_page": pagination.per_page,
            "page": pagination.page,
            "total": pagination.total}}
        return [info, marshal(bucketlists, bucketlist_fields)]


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

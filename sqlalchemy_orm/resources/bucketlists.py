from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy_orm.models import Bucketlist, db
from bucketlist_items import bucketlist_items_fields


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

    @marshal_with(bucketlist_fields)
    def get(self):
        """GET endpoint"""
        bucketlists = []
        # Bucketlist.query.all() returns a query that has to be iterated through
        for bucketlist in Bucketlist.query.all():
            bucketlists.append(bucketlist)
        return bucketlists

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

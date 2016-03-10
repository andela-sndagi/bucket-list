from flask_restful import Resource, fields, marshal_with
from app.models import Bucketlist
from bucketlist_items import bucketlist_items_fields


bucketlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'bl_items': fields.Nested(bucketlist_items_fields),
    'created_by': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
}


class Bucketlists(Resource):
    """
    Bucket List Collection [/bucketlists/]
    """
    @marshal_with(bucketlist_fields)
    def get(self):
        """GET endpoint"""
        bucketlists = []
        # Bucketlist.select() returns a query that has to be iterated through
        for bucketlist in Bucketlist.select():
            bucketlists.append(bucketlist)
        return bucketlists

    @marshal_with(bucketlist_fields)
    def post(self):
        """POST endpoint"""
        pass

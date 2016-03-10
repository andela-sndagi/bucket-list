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


class Bucketlist(Resource):
    """
    One Bucketlist
    [/bucketlists/<list_id>]
    """
    def get(self, list_id):
        """GET endpoint"""
        bucketlist = Bucketlist.get(Bucketlist.id == list_id).select()
        return bucketlist

    def put(self):
        pass

    def delete(self):
        pass

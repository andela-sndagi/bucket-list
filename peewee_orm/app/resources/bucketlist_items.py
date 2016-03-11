from flask_restful import Resource, fields, marshal_with, reqparse, marshal
from app.models import BucketlistItem


bucketlist_items_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'bucketlist_id': fields.Integer,
    'date_created': fields.String,
    'date_modified': fields.String,
    'done': fields.Boolean,
}


class BucketlistItems(Resource):
    """
    Bucketlist items
    [/bucketlists/<list_id>/items/]
    """


    # Get will be deleted eventually
    @marshal_with(bucketlist_items_fields)
    def get(self, list_id):
        """GET endpoint"""
        bucketlistitems = []
        # Bucketlist.select() returns a query that has to be iterated through
        for bucketlistitem in BucketlistItem(BucketlistItem.bucketlist_id ==
                                             list_id).select():
            bucketlistitems.append(bucketlistitem)
        return bucketlistitems

    def post(self):
        pass

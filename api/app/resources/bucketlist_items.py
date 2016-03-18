from flask_restful import Resource, fields, marshal_with, reqparse
from ..models import db, BucketlistItem


bucketlist_items_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'bucketlist': fields.Integer,
    'date_created': fields.String,
    'date_modified': fields.String,
    'done': fields.Boolean,
}


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

    # @auth.login_required
    def post(self, id):
        """post on the url"""
        args = self.parser.parse_args()
        title = args['title']
        new_bucket_list_item = BucketlistItem(title=title, bucketlist=id)
        title = new_bucket_list_item.title
        db.session.add(new_bucket_list_item)
        db.session.commit()
        return {'message': "Item '{0}' successfully created in Bucketlist #{1}".format(title, id)}, 201

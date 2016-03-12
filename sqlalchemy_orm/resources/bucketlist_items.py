from flask_restful import Resource, fields, marshal_with
from sqlalchemy_orm.models import BucketlistItem, db


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

    # Get will be deleted eventually
    @marshal_with(bucketlist_items_fields)
    def get(self, id):
        """GET endpoint"""
        bucketlistitems = []
        # Bucketlist.query. < > .all()
        # returns a query that has to be iterated through
        query = BucketlistItem.query.filter_by(bucketlist=id).all()
        for bucketlistitem in query:
            bucketlistitems.append(bucketlistitem)
        return bucketlistitems

    def post(self, id):
        new_bucket_list_item = BucketlistItem(title='Uganda', bucketlist=id)
        title = new_bucket_list_item.title
        db.session.add(new_bucket_list_item)
        db.session.commit()
        return {'message': "{} Successfully created".format(title)}, 201

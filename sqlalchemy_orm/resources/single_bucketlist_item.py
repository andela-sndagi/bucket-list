import datetime

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


class Single_BucketlistItem(Resource):
    """
    Bucketlist items
    [/bucketlists/<id>/items/<item_id>]
    """

    # Get will be deleted eventually
    @marshal_with(bucketlist_items_fields)
    def get(self, id, item_id):
        """GET endpoint"""
        bucket_list_item = BucketlistItem.query.filter_by(id=item_id, bucketlist=id).first()
        return bucket_list_item


    @marshal_with(bucketlist_items_fields)
    def put(self, id, item_id):
        """PUT endpoint"""
        bucket_list_item = BucketlistItem.query.filter_by(id=item_id, bucketlist=id).first()
        previous_title = bucket_list_item.title
        bucket_list_item.title = "5 PhD's"
        bucket_list_item.date_modified = datetime.datetime.now()
        db.session.commit()
        return {'message':
                "BucketlistItem entitled {} Successfully updated to {}".format(
                    previous_title, bucket_list_item.title)}, 200

    @marshal_with(bucketlist_items_fields)
    def delete(self, id, item_id):
        """DELETE endpoint"""
        bucket_list_item = BucketlistItem.query.filter_by(id=id).first()
        db.session.delete(bucket_list_item)
        db.session.commit()
        return {'message': "BucketlistItem entitled {} Successfully deleted".format(
            bucket_list_item.title)}, 204

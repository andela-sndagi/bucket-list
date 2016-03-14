import datetime

from flask_restful import Resource, reqparse
from sqlalchemy_orm.models import BucketlistItem, db, auth


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

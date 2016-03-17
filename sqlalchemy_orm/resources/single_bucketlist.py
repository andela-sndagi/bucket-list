import datetime

from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy_orm.models import Bucketlist
from sqlalchemy_orm.app import db, auth
from bucketlist_items import bucketlist_items_fields


bucketlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'items': fields.Nested(bucketlist_items_fields),
    'created_by': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
}


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

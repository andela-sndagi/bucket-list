import datetime

from flask_restful import Resource, fields, marshal_with
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


class Single_Bucketlist(Resource):
    """
    A Single Bucketlist [/bucketlists/<>]
    """
    @marshal_with(bucketlist_fields)
    def get(self, id):
        """GET endpoint"""
        bucketlist = Bucketlist.query.filter_by(id=id).one()
        return bucketlist

    @marshal_with(bucketlist_fields)
    def put(self, id):
        """PUT endpoint"""
        bucket_list = Bucketlist.query.filter_by(id=id).first()
        bucket_list.name = 'Academic'
        bucket_list.date_modified = datetime.datetime.now()
        db.session.commit()
        return {'message': "Bucketlist #{} Successfully created".format(bucket_list.id)}, 200

    @marshal_with(bucketlist_fields)
    def delete(self, id):
        """DELETE endpoint"""
        bucket_list = Bucketlist.query.filter_by(id=id).first()
        db.session.delete(bucket_list)
        db.session.commit()
        return {'message': "Bucketlist #{} Successfully deleted".format(bucket_list.id)}, 204

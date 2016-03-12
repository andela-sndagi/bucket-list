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


class Bucketlists(Resource):
    """
    Bucket List Collection [/bucketlists/]
    """
    @marshal_with(bucketlist_fields)
    def get(self):
        """GET endpoint"""
        bucketlists = []
        # Bucketlist.query.all() returns a query that has to be iterated through
        for bucketlist in Bucketlist.query.all():
            bucketlists.append(bucketlist)
        return bucketlists

    @marshal_with(bucketlist_fields)
    def post(self):
        """POST endpoint"""
        new_bucket_list = Bucketlist(name='Travel', created_by='Stan')
        name = new_bucket_list.name
        db.session.add(new_bucket_list)
        db.session.commit()
        return {'message': "{} Successfully created".format(name)}, 201

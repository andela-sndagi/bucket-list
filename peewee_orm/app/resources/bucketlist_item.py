from flask_restful import Resource


class BucketlistItem(Resource):
    """
    One Bucketlist item
    [/bucketlists/<list_id>/items/<item_id>]
    """

    # Get will be deleted eventually
    def get(self, list_id, item_id):
        return {'endpoint': 'BucketlistItem'}

    def put(self, list_id, item_id):
        pass

    def delete(self, list_id, item_id):
        pass
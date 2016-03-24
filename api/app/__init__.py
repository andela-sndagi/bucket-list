from flask_restful import Api
from models import app

# Resources
from resources import Index
from resources.users import Login, Register
from resources.endpoints import Bucketlists, BucketlistItems, SingleBucketlist, SingleBucketlistItem

# Instance of Api
api = Api(app)

# URLs
api.add_resource(Index, '/')
api.add_resource(Register, '/auth/register/')
api.add_resource(Login, '/auth/login/')
api.add_resource(Bucketlists, '/bucketlists/')
api.add_resource(SingleBucketlist, '/bucketlists/<int:id>')
api.add_resource(BucketlistItems, '/bucketlists/<int:id>/items/')
api.add_resource(SingleBucketlistItem, '/bucketlists/<int:id>/items/<int:item_id>')

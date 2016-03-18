# bucketlist/app.py


from flask_restful import Api
from models import app

# import ipdb; ipdb.set_trace()

# Resources
from resources.bucketlists import Bucketlists
from resources.bucketlist_items import BucketlistItems
# from resources.single_bucketlist import SingleBucketlist
# from resources.single_bucketlist_item import SingleBucketlistItem


# Instance of Api
api = Api(app)

# URLs
api.add_resource(Bucketlists, '/bucketlists/')
# api.add_resource(SingleBucketlist, '/bucketlists/<int:id>')
api.add_resource(BucketlistItems, '/bucketlists/<int:id>/items/')
# api.add_resource(SingleBucketlistItem, '/bucketlists/<int:id>/items/<int:item_id>')

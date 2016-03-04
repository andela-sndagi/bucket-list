from flask_restful import Resource

class BucketlistItems(Resource):
    def get(self):
        return {'where': 'BucketlistItems'}
    def post(self):
        pass

from flask_restful import Resource

class BucketlistItem(Resource):
    def get(self):
        return {'where': 'BucketlistItem'}
    def post(self):
        pass

from flask_restful import Resource

class Bucketlists(Resource):
    def get(self):
        return {'where': 'Bucketlists'}
    def post(self):
        pass

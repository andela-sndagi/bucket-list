from flask_restful import Resource

class Bucketlist(Resource):
    def get(self):
        return {'where': 'Bucketlist'}
    def post(self):
        pass

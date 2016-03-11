from flask_restful import Resource


class Index(Resource):
    def get(self):
        return {'status': "Bucket List Service API is ready"}

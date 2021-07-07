from flask_restful import Resource


class Index(Resource):
    """Index page"""

    def get(self):
        """GET"""
        return {'status': "Bucket List Service API is ready"}

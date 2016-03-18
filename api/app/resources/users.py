from flask import jsonify, g, abort
from flask_restful import Resource, reqparse

from ..models import User, db
# from app import db, auth


class Register(Resource):
    """
    To Register a new User
    """

    def __init__(self):
        """Instantiate route request parameters"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str,
                                 help='Enter username', location='json')
        self.parser.add_argument('password', type=str,
                                 help="User's password",
                                 location='json')
        self.parser.add_argument('conf_password', type=str,
                                 help="enter password second time to confirm",
                                 location='json')
        super(Register, self).__init__()

    def post(self):
        """POST endpoint"""
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        conf_password = args['conf_password']

        if username is None or password is None:
            abort(400) # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            abort(400)
        if password == conf_password:
            new_user = User(username=username, password=password)
            username = new_user.username
            db.session.add(new_user)
            db.session.commit()
            return {'message': "User '{}' successfully registered".format(username)}, 201
        return {"message": "Passwords don't match"}, 404

class Login(Resource):
    """
    To Login a User
    """

    def __init__(self):
        """Instantiate route request parameters"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str,
                                 help='Enter username', location='json')
        self.parser.add_argument('password', type=str,
                                 help="User's password",
                                 location='json')
        super(Login, self).__init__()

    # @auth.login_required
    def post(self):
        """POST endpoint that requires that you enter username and password"""
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).first()
        if user.verify_password(password):
            token = user.generate_auth_token()
            return jsonify({'token': token.decode('ascii')})
        return {"message": "Wrong password. Please try again"}, 404

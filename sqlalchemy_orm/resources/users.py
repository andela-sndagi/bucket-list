from flask_restful import Resource, reqparse
from sqlalchemy_orm.models import User, db


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
        if password == conf_password:
            new_user = User(username=username, password=password)
            username = new_user.username
            db.session.add(new_user)
            db.session.commit()
            return {'message': "User '{}' Successfully registered".format(username)}, 201
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

    def post(self):
        """POST endpoint"""
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).one()
        if user.verify_password(password):
            token = user.generate_token()
            return {'token': token.decode('ascii')}, 200
        return {"message": "Wrong password. Please try again"}, 404

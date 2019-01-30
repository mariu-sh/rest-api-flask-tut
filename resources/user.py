import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Username cannot be empty")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Password cannot be empty')

    def username_already_exists(self, username):
        return True if UserModel.find_by_username(username) else False

    def post(self):
        data = User.parser.parse_args()

        if self.username_already_exists(data['username']):
            return {"message": "Username already exists in DB"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201

from os import getenv
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import authenticate, identity

from resources.item import Item, ItemList
from resources.user import User
from resources.store import Store, StoreList

# INIT APP
app = Flask(__name__)

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.before_first_request
def create_tables():
    db.create_all()

# JWT CONFIG
app.secret_key = 'jose'
jwt = JWT(app, authenticate, identity) # /auth

# API CONFIG
api = Api(app)
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/register')

if __name__ == "__main__":
    from db import db # IMPORT HERE TO AVOID CONCURENT IMPORT IN MODELS
    db.init_app(app)
    app.run(port=5000, debug=False)

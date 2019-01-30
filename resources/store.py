from flask_restful import Resource
from flask_jwt import jwt_required

from models.store_model import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json
        return {'message': "Store not found"}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store {0} already exists'.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "Could not save store"}, 500
        return store.json, 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store {0} deleted/does not exist'.format(name)}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': StoreModel.get_all()}

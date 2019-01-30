from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item_model import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        data = Item.parser.parse_args()

        if ItemModel.find_by_name(name):
            return {'message': 'Item with name {} already exists'.format(name)}

        item = ItemModel(name=name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred during inserting item'}, 500

        return item.json, 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete_from_db()
                return {'message': "Item deleted"}
            except:
                return {'message': "Item could not be deleted"}, 500
        return {"message": "Item not found"}, 404

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name=name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json, 201


class ItemList(Resource):
    def get(self):
        return {'items': ItemModel.get_all()}

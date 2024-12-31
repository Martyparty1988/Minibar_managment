from flask import Blueprint, request, jsonify
from app import db
from models import Item, Order
from export_utils import export_csv

api = Blueprint('api', __name__)

# CRUD: Items
@api.route('/items', methods=['GET', 'POST'])
def manage_items():
    if request.method == 'GET':
        items = Item.query.all()
        return jsonify([{"id": i.id, "name": i.name, "price": i.price, "quantity": i.quantity} for i in items])

    if request.method == 'POST':
        data = request.get_json()
        new_item = Item(name=data['name'], price=data['price'], quantity=data['quantity'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item added!"}), 201

@api.route('/items/<int:item_id>', methods=['PUT', 'DELETE'])
def update_delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == 'PUT':
        data = request.get_json()
        item.name = data['name']
        item.price = data['price']
        item.quantity = data['quantity']
        db.session.commit()
        return jsonify({"message": "Item updated!"})

    if request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted!"})

# Analytics
@api.route('/analytics/items', methods=['GET'])
def item_analytics():
    items = Item.query.all()
    analytics = [{"name": i.name, "quantity": i.quantity, "total_value": i.quantity * i.price} for i in items]
    return jsonify(analytics)

@api.route('/analytics/export', methods=['GET'])
def export_analytics():
    items = Item.query.all()
    data = [{"name": i.name, "quantity": i.quantity, "total_value": i.quantity * i.price} for i in items]
    csv_path = export_csv(data)
    return jsonify({"message": "Export successful!", "file": csv_path})
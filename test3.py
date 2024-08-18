from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

# Sample data using UID hash instead of integer ID
items = [
    {"id": str(uuid.uuid4()), "name": "Item 1"},
    {"id": str(uuid.uuid4()), "name": "Item 2"},
    {"id": str(uuid.uuid4()), "name": "Item 3"}
]

# GET method to retrieve all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# GET method to retrieve a single item by UID
@app.route('/items/<id>', methods=['GET'])
def get_item(uid):
    item = next((item for item in items if item["id"] == id), None)
    if item is not None:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# POST method to add a new item with a UID
@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    new_item["id"] = str(uuid.uuid4())  # Generate a new UUID
    items.append(new_item)
    return jsonify(new_item), 201

# DELETE method to delete an item by UID
@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    global items
    items = [item for item in items if item["id"] != id]
    return jsonify({"message": "Item deleted"}), 200

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

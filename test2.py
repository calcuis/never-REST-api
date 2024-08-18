from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"}
]

# GET method to retrieve all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# GET method to retrieve a single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is not None:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# POST method to add a new item
@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    new_item["id"] = len(items) + 1  # Auto-increment ID
    items.append(new_item)
    return jsonify(new_item), 201

# DELETE method to delete an item by ID
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

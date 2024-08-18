from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlotte"}
]

# Endpoint to get all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data)

# Endpoint to get a specific item by ID
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = next((item for item in data if item["id"] == id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"message": "Item not found"}), 404

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

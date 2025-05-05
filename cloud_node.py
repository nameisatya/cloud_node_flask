# cloud_node.py

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
AGGREGATED_PATH = "aggregated_updates.json"

# Route to receive data from the Fog Node
@app.route('/receive_from_fog', methods=['POST'])
def receive_from_fog():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Initialize the JSON file if it doesn't exist
    if not os.path.exists(AGGREGATED_PATH):
        with open(AGGREGATED_PATH, "w") as f:
            json.dump([], f)

    # Load existing data and append the new one
    with open(AGGREGATED_PATH, "r+", encoding="utf-8") as f:
        try:
            existing = json.load(f)
        except json.JSONDecodeError:
            existing = []

        existing.append(data)
        f.seek(0)
        json.dump(existing, f, indent=4)
        f.truncate()

    return jsonify({"message": "Data received from Fog Node"}), 200

# Route to confirm the server is live
@app.route('/', methods=['GET'])
def home():
    return "✅ Cloud Node is running!"

# Route to view all saved updates
@app.route('/view_data', methods=['GET'])
def view_data():
    if not os.path.exists(AGGREGATED_PATH):
        return jsonify({"message": "No data found."}), 404

    with open(AGGREGATED_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return jsonify({"error": "Data is corrupted or empty."}), 500

    return jsonify(data), 200

# Run the app on the correct port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)




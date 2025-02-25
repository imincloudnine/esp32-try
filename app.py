from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Koneksi ke MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sensor_db"]
collection = db["dht_data"]

@app.route('/api/sensor', methods=['POST'])
def receive_data():
    data = request.json
    if "temperature" in data and "humidity" in data:
        collection.insert_one(data)
        return jsonify({"message": "Data saved successfully"}), 200
    return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

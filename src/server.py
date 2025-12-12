import json
import os
import requests
import shutil
import time
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
DATA_FILE = 'clients.json'

# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

# 1. Main Route: Serve index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 2. File Route
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

# 3. API: Get Clients
@app.route('/api/clients', methods=['GET'])
def get_clients():
    if not os.path.exists(DATA_FILE):
        return jsonify([])
    with open(DATA_FILE, 'r') as f:
        return jsonify(json.load(f))

# 4. API: Add Client
@app.route('/api/clients', methods=['POST'])
def add_client():
    new_client = request.json
    
    # Geocoding
    if 'address' in new_client and (not new_client.get('lat') or not new_client.get('lng')):
        print(f"Resolving address: {new_client['address']}")
        try:
            headers = { 'User-Agent': 'MSP_VPN_Map_Tool/1.0' }
            resp = requests.get("https://nominatim.openstreetmap.org/search", 
                              params={'q': new_client['address'], 'format': 'json', 'limit': 1},
                              headers=headers)
            if resp.status_code == 200 and resp.json():
                new_client['lat'] = float(resp.json()[0]['lat'])
                new_client['lng'] = float(resp.json()[0]['lon'])
            else:
                return jsonify({"error": "Address not found"}), 400
        except Exception as e:
            print(f"Geocoding Error: {e}")
            return jsonify({"error": "Geocoding failed"}), 500

    # Load & Append
    clients = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            clients = json.load(f)
    clients.append(new_client)
    
    # Backup
    if os.path.exists(DATA_FILE):
        shutil.copy(DATA_FILE, 'clients.backup.json')

    # Save
    with open(DATA_FILE, 'w') as f:
        json.dump(clients, f, indent=2)
    
    return jsonify({"message": "Saved", "client": new_client})

# 5. API: Delete Client
@app.route('/api/clients/<name>', methods=['DELETE'])
def delete_client(name):
    if os.path.exists(DATA_FILE):
        shutil.copy(DATA_FILE, 'clients.backup.json')
        with open(DATA_FILE, 'r') as f:
            clients = json.load(f)
        clients = [c for c in clients if c['name'] != name]
        with open(DATA_FILE, 'w') as f:
            json.dump(clients, f, indent=2)
    return jsonify({"message": "Deleted"})

if __name__ == '__main__':
    print("Starting Server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Conectar ao MongoDB no Railway
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://aleonam321:g9wHdtWTrOOWHe4X@keys.w14wzx0.mongodb.net/?retryWrites=false&w=majority")
client = MongoClient(MONGO_URI)
db = client['keys']
collection = db['keys']

@app.route('/generate-key', methods=['POST'])
def generate_key():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        days = data.get('days')

        if not user_id or not days:
            return jsonify({'status': 'error', 'message': 'user_id e days são necessários'}), 400

        key = f'{user_id}-{days}'
        collection.insert_one({'user_id': user_id, 'days': days, 'key': key})

        return jsonify({'key': key, 'status': 'success'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get-keys', methods=['GET'])
def get_keys():
    try:
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({'status': 'error', 'message': 'user_id é necessário'}), 400

        keys = list(collection.find({'user_id': user_id}, {'_id': 0}))

        if not keys:
            return jsonify({'status': 'error', 'message': 'Nenhuma chave encontrada'}), 404

        return jsonify({'keys': keys, 'status': 'success'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

# Load environment variables dari .env
load_dotenv()

# Ambil API Key dari .env
API_NINJA_KEY = os.getenv("API_NINJA_KEY")
API_URL = "https://api.api-ninjas.com/v1/nutrition?query="

# Buat Blueprint untuk routes
food_bp = Blueprint('food', __name__)

@food_bp.route('/foods', methods=['GET'])
def get_foods():
    """ Endpoint untuk mengambil informasi nutrisi makanan dari API Ninja """
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify([])  # Balikin array kosong kalau query kosong

    headers = {'X-Api-Key': API_NINJA_KEY}
    response = requests.get(API_URL + query, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())  # Balikin data dari API Ninja
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

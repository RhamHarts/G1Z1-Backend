from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Ambil API Key dari .env
API_NINJA_KEY = os.getenv("API_NINJA_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")

food_bp = Blueprint("food", __name__)

@food_bp.route("/foods", methods=["GET"])
def get_foods():
    """ Fetch data makanan dari API Ninja """
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify([])

    API_URL = "https://api.api-ninjas.com/v1/nutrition?query=" + query
    headers = {"X-Api-Key": API_NINJA_KEY}
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

@food_bp.route("/unsplash", methods=["GET"])
def get_unsplash_image():
    """ Fetch gambar dari Unsplash """
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query is required"}), 400

    unsplash_url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_API_KEY}"
    response = requests.get(unsplash_url)

    if response.status_code == 200:
        data = response.json()
        image_url = data["results"][0]["urls"]["small"] if data["results"] else "/images/default.jpg"
        return jsonify({"image": image_url})
    else:
        return jsonify({"error": "Failed to fetch image"}), response.status_code

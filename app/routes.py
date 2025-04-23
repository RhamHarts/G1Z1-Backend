from flask import Blueprint, abort, request, jsonify,send_from_directory
import requests
import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from app.models import db, LocalFood
from werkzeug.utils import secure_filename,safe_join
load_dotenv()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Ambil API Key dari .env
API_NINJA_KEY = os.getenv("API_NINJA_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")

food_bp = Blueprint("food", __name__)

@food_bp.route("/foods", methods=["GET"])
def get_foods():
    """ Cari makanan dari API Ninja, jika tidak ada ambil dari database lokal """
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify([])

    # 🔹 Cek API Ninja dulu
    API_URL = "https://api.api-ninjas.com/v1/nutrition?query=" + query
    headers = {"X-Api-Key": API_NINJA_KEY}
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 200:
        api_data = response.json()
        if api_data:
            return jsonify(api_data)

    # 🔹 Jika tidak ditemukan di API Ninja, cek database lokal
    local_foods = LocalFood.query.filter(LocalFood.name.ilike(f"%{query}%")).all()
    if local_foods:
        return jsonify([food.to_dict() for food in local_foods])

    return jsonify({"error": "Makanan tidak ditemukan"}), 404

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
@food_bp.route("/local-foods", methods=["GET"])
def get_local_foods():
    """ Mengambil semua makanan dari database lokal """
    foods = LocalFood.query.all()
    return jsonify([food.to_dict() for food in foods])

@food_bp.route("/local-foods", methods=["POST"])
def add_multiple_local_foods():
    """ Menambahkan banyak makanan ke database dalam satu request """
    data = request.json  # Data dari request body

    # Pastikan data berupa list
    if not isinstance(data, list):
        return jsonify({"error": "Data harus berupa list"}), 400

    new_foods = []
    for food in data:
        if not all(k in food for k in (  "name", "carbohydrates_total_g", "cholesterol_mg", "fat_saturated_g",
            "fat_total_g", "fiber_g", "potassium_mg", "sodium_mg", "sugar_g", "protein_g")):
            return jsonify({"error": "Data tidak lengkap"}), 400

        new_food = LocalFood(
             name=food["name"],
            carbohydrates_total_g=food["carbohydrates_total_g"],
            cholesterol_mg=food["cholesterol_mg"],
            fat_saturated_g=food["fat_saturated_g"],
            fat_total_g=food["fat_total_g"],
            fiber_g=food["fiber_g"],
            potassium_mg=food["potassium_mg"],
            sodium_mg=food["sodium_mg"],
            sugar_g=food["sugar_g"],
            protein_g=food["protein_g"]
        )
        new_foods.append(new_food)

    # Tambahkan semua makanan ke database sekaligus
    db.session.bulk_save_objects(new_foods)
    db.session.commit()

    return jsonify({"message": "Semua makanan berhasil ditambahkan!", "total_added": len(new_foods)}), 201
def allowed_file(filename):
    """ Cek apakah file gambar memiliki ekstensi yang diizinkan """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@food_bp.route("/local-foods/upload", methods=["POST"])
def upload_food_image():
    """ Upload gambar makanan dan simpan path-nya di database """
    if "image" not in request.files:
        return jsonify({"error": "Tidak ada file yang diunggah"}), 400

    file = request.files["image"]
    food_id = request.form.get("food_id")  # Ambil ID makanan dari form

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "Format file tidak didukung"}), 400

    if not food_id:
        return jsonify({"error": "food_id diperlukan"}), 400

    food = LocalFood.query.get(food_id)
    if not food:
        return jsonify({"error": "Makanan tidak ditemukan"}), 404

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)  # Simpan file di server

    # Update database dengan path gambar
    food.image = file_path
    db.session.commit()

    return jsonify({"message": "Gambar berhasil diunggah!", "image_path": file_path}), 200

@food_bp.route("/local-foods/<int:food_id>", methods=["DELETE"])
def delete_local_food(food_id):
    """ Menghapus makanan berdasarkan ID """
    food = LocalFood.query.get(food_id)

    if not food:
        return jsonify({"error": "Makanan tidak ditemukan"}), 404

    db.session.delete(food)
    db.session.commit()

    return jsonify({"message": f"Makanan '{food.name}' berhasil dihapus!"}), 200

@food_bp.route("/uploads/<filename>")
def get_uploaded_file(filename):
    """ Menampilkan gambar dari folder uploads """
    upload_folder = os.path.join(os.getcwd(), "uploads")  # Path absolute ke folder uploads
    file_path = safe_join(upload_folder, filename)  # Menghindari akses di luar folder

    if not os.path.exists(file_path):  # Cek apakah file ada
        abort(404)  # Jika tidak ada, return 404
    
    return send_from_directory(upload_folder, filename)
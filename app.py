from app import create_app
from flask import send_from_directory
import os

app = create_app()

# Route untuk halaman utama
@app.route("/")
def home():
    return "Backend API!", 200

# Route untuk melayani gambar dari folder uploads
@app.route("/uploads/<filename>")
def get_uploaded_file(filename):
    """ Menampilkan gambar dari folder uploads """
    upload_folder = os.path.join(os.getcwd(), "uploads")  # Ambil path absolute ke folder uploads
    return send_from_directory(upload_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

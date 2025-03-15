import os
import sys

# Tambahkan path ke dalam sys.path agar Flask bisa menemukan modul config
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.routes import food_bp
from app.models import db

def create_app():
    app = Flask(__name__)

    # Pastikan Flask bisa menemukan config.py
    try:
        app.config.from_object("config.Config")
    except ImportError:
        app.config.from_object("app.config.Config")

    CORS(app)
    
    db.init_app(app)

    # Buat tabel database jika belum ada
    with app.app_context():
        db.create_all()

    app.register_blueprint(food_bp, url_prefix='/api')

    return app

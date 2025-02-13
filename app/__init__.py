from flask import Flask
from flask_cors import CORS
from app.routes import food_bp  # Import blueprint dari routes.py

def create_app():
    app = Flask(__name__)
    CORS(app)  # Supaya bisa diakses dari frontend

    # Register Blueprint
    app.register_blueprint(food_bp, url_prefix='/api')

    return app

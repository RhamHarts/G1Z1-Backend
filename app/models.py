from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LocalFood(db.Model):
    __tablename__ = "local_foods"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    carbohydrates_total_g = db.Column(db.Float, nullable=False)
    cholesterol_mg = db.Column(db.Float, nullable=False)
    fat_saturated_g = db.Column(db.Float, nullable=False)
    fat_total_g = db.Column(db.Float, nullable=False)
    fiber_g = db.Column(db.Float, nullable=False)
    potassium_mg = db.Column(db.Float, nullable=False)
    sodium_mg = db.Column(db.Float, nullable=False)
    sugar_g = db.Column(db.Float, nullable=False)
    protein_g = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=True)  # Path gambar di database

    def to_dict(self):
        """ Mengubah objek LocalFood menjadi dictionary JSON """
        image_path = self.image.replace("\\", "/") if self.image else None  # Fix path Windows
    
        # Pastikan path tidak ada double "uploads/uploads/"
        if image_path and image_path.startswith("uploads/"):
            image_path = image_path.replace("uploads/", "", 1)

        return {
            "id": self.id,
            "name": self.name,
            "carbohydrates_total_g": self.carbohydrates_total_g,
            "cholesterol_mg": self.cholesterol_mg,
            "fat_saturated_g": self.fat_saturated_g,
            "fat_total_g": self.fat_total_g,
            "fiber_g": self.fiber_g,
            "potassium_mg": self.potassium_mg,
            "sodium_mg": self.sodium_mg,
            "sugar_g": self.sugar_g,
            "protein_g": self.protein_g,
            "image": f"http://127.0.0.1:5001/uploads/{image_path}" if image_path else None
        }

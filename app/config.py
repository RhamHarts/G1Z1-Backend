import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:yourpassword@localhost/G1Z1_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
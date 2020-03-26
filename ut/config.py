import os


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAP_KEY = os.environ.get("GOOGLE_MAP_API")

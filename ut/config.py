import os


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAP_KEY = os.getenv("GOOGLE_MAP_API")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config_Tester:
    SECRET_KEY = "this the test key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database_test_site.db"
    BCRYPT_LOG_ROUNDS = 4

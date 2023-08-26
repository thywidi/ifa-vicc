import os
from dotenv import load_dotenv

baseDir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(baseDir, ".env"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "not_so_secret_key"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATEBASE_URL"
    ) or "sqlite:///" + os.path.join(baseDir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

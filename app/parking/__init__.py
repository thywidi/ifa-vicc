from flask import Blueprint

bp = Blueprint("parking", __name__)

from app.parking import routes  # noqa: E402, F401

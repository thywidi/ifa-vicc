from flask import jsonify
from app.models import ParkingSpot
from app.api import bp
from app.api.auth import token_auth


@bp.route("/spots/<int:id>", methods=["GET"])
@token_auth.login_required
def get_spot(id):
    return jsonify(ParkingSpot.query.get_or_404(id).to_dict())


@bp.route("/spots", methods=["GET"])
@token_auth.login_required
def get_spots():
    data = ParkingSpot.to_collection_dict(ParkingSpot.query)
    return jsonify(data)


@bp.route("/spots/<int:id>/get_spot_reservations", methods=["GET"])
@token_auth.login_required
def get_spot_reservations(id):
    spot = ParkingSpot.query.get_or_404(id)
    data = ParkingSpot.to_collection_dict(spot.reservations)
    return jsonify(data)


@bp.route("/spots/<int:id>/get_spot_reserved", methods=["GET"])
@token_auth.login_required
def get_spot_reserved(id):
    spot = ParkingSpot.query.get_or_404(id)
    return jsonify(spot.is_reserved())

from flask import jsonify
from app.models import Reservation, ParkingSpot, User
from app.api import bp
from app.api.auth import token_auth


@bp.route("/reservations/<int:id>", methods=["GET"])
@token_auth.login_required
def get_reservation(id):
    return jsonify(Reservation.query.get_or_404(id).to_dict())


@bp.route("/reservations", methods=["GET"])
@token_auth.login_required
def get_reservations():
    data = Reservation.to_collection_dict(Reservation.query)
    return jsonify(data)


@bp.route("/reservations/<int:id>/get_reservation_user", methods=["GET"])
@token_auth.login_required
def get_reservation_user(id):
    reservation = Reservation.query.get_or_404(id)
    user = User.query.get_or_404(reservation.user_id)
    return jsonify(user)


@bp.route("/reservations/<int:id>/get_reservation_spot", methods=["GET"])
@token_auth.login_required
def get_reservation_spot(id):
    reservation = Reservation.query.get_or_404(id)
    spot = ParkingSpot.query.get_or_404(reservation.parking_spot_id)
    return jsonify(spot)

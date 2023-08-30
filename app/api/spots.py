import datetime
from flask import jsonify, abort
from app.models import ParkingSpot
from app.api import bp
from app.api.auth import token_auth


@bp.route("/spots/<int:id>", methods=["GET"])
@token_auth.login_required
def get_spot(id):
    """
    @api {get} /spot/:id Gets a spot
    @apiVersion 1.0.0
    @apiName spots
    @apiGroup Spots

    @apiParam {Number}      id              The spots's i

    @apiExample Example usage:
    curl -i http://localhost/spots

    @apiSuccess {Object}    spots                 The user data
    @apiSuccess {Number}    spots.id              The user's id.
    @apiSuccess {String}    spots.info        The user's username.
    @apiSuccess {Number}    spots.price      The first name of the User.
    @apiSuccess {Number}    spots.reservation_count       The last name of the User.
    @apiSuccess {Object}    spots.links         The profile data
    @apiSuccess {String}    spots.links.age     The user's age.
    @apiSuccess {String}    spots.links.reserved     The user's age.
    @apiSuccess {String}    spots.links.self     The user's age.
    """
    return jsonify(ParkingSpot.query.get_or_404(id).to_dict())


@bp.route("/spots", methods=["GET"])
def get_spots():
    data = ParkingSpot.to_collection_dict(ParkingSpot.query)
    return jsonify(data)


@bp.route("/spots/<int:id>/get_spot_reservations", methods=["GET"])
@token_auth.login_required
def get_spot_reservations(id):
    spot = ParkingSpot.query.get_or_404(id)
    data = ParkingSpot.to_collection_dict(spot.reservations)
    return jsonify(data)


@bp.route("/spots/<int:id>/get_spot_reserved/<date>", methods=["GET"])
@token_auth.login_required
def get_spot_reserved(id, date):
    try:
        dateObj = datetime.date.fromisoformat(date)
    except ValueError:
        abort(404)

    spot = ParkingSpot.query.get_or_404(id)
    reservation = spot.is_reserved(dateObj)
    if reservation:
        return jsonify(reservation.to_dict())
    return jsonify(False)

import datetime
from flask import jsonify, abort
from app.models import ParkingSpot
from app.api import bp
from app.api.auth import token_auth


@bp.route("/spots/<int:id>", methods=["GET"])
@token_auth.login_required
def get_spot(id):
    """
    @api {get} api/spots/:id Gets a spot
    @apiVersion 1.0.0
    @apiName get_spot
    @apiGroup Spots

    @apiParam {Number}      id              The spots's id

    @apiExample Example usage:
    curl -i http://127.0.0.1:500/api/spots/1

    @apiSuccess {Number}    id              The spot's id.
    @apiSuccess {String}    info        The spot's info text.
    @apiSuccess {Number}    price      The price of the spot.
    @apiSuccess {Object}    links         Self Links
    @apiSuccess {String}    links.self      Spot details
    @apiSuccess {Object}    links.reservations     All Reservations of the spot
    @apiSuccess {String}    links.reserved     If the spot is reserved
    """
    return jsonify(ParkingSpot.query.get_or_404(id).to_dict())


@bp.route("/spots", methods=["GET"])
def get_spots():
    """
    @api {get} api/spots/ Gets all spots
    @apiVersion 1.0.0
    @apiName get_spots
    @apiGroup Spots

    @apiExample Example usage:
    curl -i http://127.0.0.1:500/api/spots

    @apiSuccess {Object}    spots                 The spot data
    @apiSuccess {Number}    spots.id              The spot's id.
    @apiSuccess {String}    spots.info        The spot's info text.
    @apiSuccess {Number}    spots.price      The price of the spot.
    @apiSuccess {Object}    spots.links         Self Links
    @apiSuccess {String}    spots.links.self      Spot details
    @apiSuccess {Object}    spots.links.reservations     All Reservations of the spot
    @apiSuccess {String}    spots.links.reserved     If the spot is reserved
    """
    data = ParkingSpot.to_collection_dict(ParkingSpot.query)
    return jsonify(data)


@bp.route("/spots/<int:id>/get_spot_reservations", methods=["GET"])
@token_auth.login_required
def get_spot_reservations(id):
    """
    @api {get} api/spots/:id/get_spot_reservations Get all reservations for spot
    @apiVersion 1.0.0
    @apiName get_spot_reservations
    @apiGroup Spots

    @apiExample Example usage:
    curl -i http://127.0.0.1:500/api/spots/1/get_spot_reservations

    @apiParam {Number}      id              The spots's id

    @apiSuccess {Object}    reservations                 The spot reservations
    """
    spot = ParkingSpot.query.get_or_404(id)
    data = ParkingSpot.to_collection_dict(spot.reservations)
    return jsonify(data)


@bp.route("/spots/<int:id>/get_spot_reserved/<date>", methods=["GET"])
@token_auth.login_required
def get_spot_reserved(id, date):
    """
    @api {get} api/spots/:id/get_spot_reserved Get the reservation status of a spot
    @apiVersion 1.0.0
    @apiName get_spot_reserved
    @apiGroup Spots

    @apiExample Example usage:
    curl -i http://127.0.0.1:500/api/spots/1/get_spot_reserved

    @apiParam {Number}      id              The spots's id

    @apiSuccess {Boolean}    reserved                 If the spot is reserved
    """
    try:
        dateObj = datetime.date.fromisoformat(date)
    except ValueError:
        abort(404)

    spot = ParkingSpot.query.get_or_404(id)
    reservation = spot.is_reserved(dateObj)
    if reservation:
        return jsonify(True)
    return jsonify(False)

from flask import jsonify
from app.models import Reservation, ParkingSpot, User
from app.api import bp
from app.api.auth import token_auth


@bp.route("/reservations/<int:id>", methods=["GET"])
@token_auth.login_required
def get_reservation(id):
    """
    @api {get} /api/reservations/:id Gets a reservation
    @apiVersion 1.0.0
    @apiName get_reservation
    @apiGroup Reservations

    @apiParam {Number}      id              The reservations's id

    @apiExample Example usage:
    curl -i http://127.0.0.1:500/api/reservations/1

    @apiSuccess {Number}    id              The reservation's id.
    @apiSuccess {String}    date        The reservation's date.
    @apiSuccess {Number}    parking_spot_id      Id of the reserved parking spot
    @apiSuccess {Number}    user_id      Id of the user who reserved the parking spot
    @apiSuccess {Object}    links         Self Links
    @apiSuccess {String}    links.self      Reservation details
    @apiSuccess {Object}    links.user     User informations
    @apiSuccess {String}    links.spot     Spot Informations
    """
    return jsonify(Reservation.query.get_or_404(id).to_dict())


@bp.route("/reservations", methods=["GET"])
def get_reservations():
    """
    @api {get} /api/reservations Gets all reservations
    @apiVersion 1.0.0
    @apiName get_reservations
    @apiGroup Reservations

    @apiExample Example usage:
    curl -i http://127.0.0.1:500/api/reservations

    @apiSuccess {Object}    reservations         Reservations
    @apiSuccess {Number}    reservations.id              The reservation's id.
    @apiSuccess {String}    reservations.date        The reservation's date.
    @apiSuccess {Number}    reservations.parking_spot_id      Id of the reserved parking spot
    @apiSuccess {Number}    reservations.user_id      Id of the user who reserved the parking spot
    @apiSuccess {Object}    reservations.links         Self Links
    @apiSuccess {String}    reservations.links.self      Reservation details
    @apiSuccess {Object}    reservations.links.user     User informations
    @apiSuccess {String}    reservations.links.spot     Spot Informations
    """
    data = Reservation.to_collection_dict(Reservation.query)
    return jsonify(data)


@bp.route("/reservations/<int:id>/get_reservation_user", methods=["GET"])
@token_auth.login_required
def get_reservation_user(id):
    """
    @api {get} api/reservations/:id/get_reservation_user Gets a User from a reservation
    @apiVersion 1.0.0
    @apiName get_reservation_user
    @apiGroup Reservations

    @apiParam {Number}      id              The reservations's id

    @apiExample Example usage:
    curl -i http://127.0.0.1:500/api/get_reservation_user/1

    @apiSuccess {Number}    id              The user's id.
    @apiSuccess {String}    username              The user's username.
    """
    reservation = Reservation.query.get_or_404(id)
    user = User.query.get_or_404(reservation.user_id)
    return jsonify(user.to_dict())


@bp.route("/reservations/<int:id>/get_reservation_spot", methods=["GET"])
@token_auth.login_required
def get_reservation_spot(id):
    """
    @api {get} api/reservations/:id/get_reservation_spot Gets a Spot from a reservation
    @apiVersion 1.0.0
    @apiName get_reservation_spot
    @apiGroup Reservations

    @apiParam {Number}      id              The reservations's id

    @apiExample Example usage:
    curl -i http://127.0.0.1:500/api/get_reservation_spot/1

    @apiSuccess {Number}    id              The spot's id.
    @apiSuccess {String}    info        The spot's info text.
    @apiSuccess {Number}    price      The price of the spot.
    @apiSuccess {Object}    links         Self Links
    @apiSuccess {String}    links.self      Spot details
    @apiSuccess {Object}    links.reservations     All Reservations of the spot
    @apiSuccess {String}    links.reserved     If the spot is reserved
    """
    reservation = Reservation.query.get_or_404(id)
    spot = ParkingSpot.query.get_or_404(reservation.parking_spot_id)
    return jsonify(spot.to_dict())

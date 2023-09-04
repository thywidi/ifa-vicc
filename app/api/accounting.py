import datetime
from flask import jsonify
from sqlalchemy import select
from app.models import Reservation, ParkingSpot, User
from app.api import bp
from app.api.auth import token_auth
from app import db


@bp.route("/accounting", methods=["GET"])
@token_auth.login_required
def get_accounting():
    """
    @api {get} /api/accounting   Get accounting data until current day
    @apiVersion 1.0.0
    @apiName get_accounting
    @apiGroup Accounting

    @apiExample Example usage:
    curl -i http://165.22.31.195/api/accounting

    @apiSuccess {Number}    spots                Total Spots
    @apiSuccess {Number}    occupied             Occupied spots count
    @apiSuccess {Number}    occupation           Occupation in float
    @apiSuccess {Number}    revenue              Revevenue
    """
    spots = db.session.scalars(select(ParkingSpot)).all()
    spotCount = len(list(spots))
    today = datetime.date.today()
    occupied = len(list(filter(lambda x: x.is_reserved(today), spots)))
    occupation = round((occupied / spotCount), 2)

    reservations = db.session.scalars(
        select(Reservation)
        .filter(Reservation.date <= today)
        .join(ParkingSpot)
        .join(User)
    ).all()

    revenue = sum(map(lambda x: x.parking_spot.price, reservations))
    return jsonify(
        {
            "spots": spotCount,
            "occupied": occupied,
            "occupation": occupation,
            "revenue": revenue,
        }
    )

from flask import flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required
from sqlalchemy import select
from app.models import ParkingSpot, Reservation, User
from app import db
from app.parking import bp
from app.parking.calendar import ParkingCalendar
from app.parking.forms import BaseForm
import datetime

Calendar = ParkingCalendar()


@bp.route("/")
@login_required
def index():
    form = BaseForm()

    year = datetime.date.today().year
    month = datetime.date.today().month
    today = datetime.date.today()

    spots = db.session.scalars(select(ParkingSpot))

    return render_template(
        "pages/index.html",
        title="Home",
        year=year,
        month=month,
        activeDate=today,
        today=today,
        weeks=Calendar.get_days(month, year),
        spots=spots,
        form=form,
    )


@bp.route("/<date>")
@login_required
def date(date):
    form = BaseForm()
    try:
        activeDate = datetime.date.fromisoformat(date)
    except ValueError:
        abort(404)

    today = datetime.date.today()
    if activeDate < today:
        abort(404)

    year = datetime.date.today().year
    month = datetime.date.today().month
    spots = db.session.scalars(select(ParkingSpot))

    return render_template(
        "pages/index.html",
        title="Home",
        year=year,
        month=month,
        today=today,
        activeDate=activeDate,
        weeks=Calendar.get_days(month, year),
        spots=spots,
        form=form,
    )


@bp.route("/reserve/<spot>/<day>", methods=["POST"])
@login_required
def reserve(spot, day):
    form = BaseForm()
    today = datetime.date.today()
    dayDate = datetime.date.fromisoformat(day)
    if form.validate_on_submit():
        if dayDate < today:
            flash("Cannot make reservations in the past")
            return redirect(url_for("parking.index"))

        # TODO: Error handling and testing
        spot = ParkingSpot.query.filter_by(id=spot).first()

        if spot is None:
            flash(f"Spot {spot} not found.")
            return redirect(url_for("parking.index"))

        user = User.query.filter_by(id=current_user.id).first()  # type: ignore
        if user is None:
            raise ValueError("User not found")

        if user.reservation(dayDate):
            flash(
                "Cannot reserve spot. You can only have 1 reservaton per day", "error"
            )
            return redirect(url_for("parking.index"))

        spot.reserve(day, current_user)
        flash(f"Spot {spot} reserved!")
        db.session.commit()

        return redirect(url_for("parking.index"))
    else:
        return redirect(url_for("parking.index"))


@bp.route("/free/<spot>/<day>", methods=["POST"])
@login_required
def free(spot, day):
    form = BaseForm()
    today = datetime.date.today()
    dayDate = datetime.date.fromisoformat(day)
    if form.validate_on_submit():
        if dayDate < today:
            flash("Cannot make changes to reservations in the past")
            return redirect(url_for("parking.index"))

        # TODO: Error handling and testing
        spot = ParkingSpot.query.filter_by(id=spot).first()
        if spot is None:
            flash(f"Spot {spot} not found.")
            return redirect(url_for("parking.index"))

        userReservation = spot.free(day, current_user)
        if userReservation is not None:
            db.session.delete(userReservation)
            db.session.commit()
            flash(f"Spot {spot} is now free!")
        else:
            flash(f"Spot {spot} is not reserved by you.", "error")
        return redirect(url_for("parking.index"))
    else:
        return redirect(url_for("parking.index"))


@bp.route("/accounting")
@login_required
def accounting():
    spots = db.session.scalars(select(ParkingSpot)).all()
    spotCount = len(list(spots))
    today = datetime.date.today()
    occupied = len(list(filter(lambda x: x.is_reserved(today), spots)))
    occupation = round((occupied / spotCount) * 100, 2)

    reservations = db.session.scalars(
        select(Reservation)
        .filter(Reservation.date <= today)
        .join(ParkingSpot)
        .join(User)
    ).all()

    revenue = sum(map(lambda x: x.parking_spot.price, reservations))

    return render_template(
        "pages/accounting.html",
        title="Accounting",
        spots=spotCount,
        occupied=occupied,
        occupation=occupation,
        reservations=reservations,
        revenue=revenue,
    )

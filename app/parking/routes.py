from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from app.models import ParkingSpot
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
        weeks=Calendar.get_days(month, year),
        spots=spots,
        form=form,
    )


@bp.route("/<date>")
@login_required
def date(date):
    form = BaseForm()

    year = datetime.date.today().year
    month = datetime.date.today().month
    spots = db.session.scalars(select(ParkingSpot))

    return render_template(
        "pages/index.html",
        title="Home",
        year=year,
        month=month,
        activeDate=date,
        weeks=Calendar.get_days(month, year),
        spots=spots,
        form=form,
    )


@bp.route("/reserve/<spot>/<day>", methods=["POST"])
@login_required
def reserve(spot, day):
    form = BaseForm()
    if form.validate_on_submit():
        # TODO: Error handling and testing
        spot = ParkingSpot.query.filter_by(id=spot).first()
        if spot is None:
            flash(f"Spot {spot} not found.")
            return redirect(url_for("parking.index"))
        spot.reserve(day, current_user)
        db.session.commit()
        flash(f"Spot {spot} reserved!")
        return redirect(url_for("parking.index"))
    else:
        return redirect(url_for("parking.index"))


@bp.route("/free/<spot>/<day>", methods=["POST"])
@login_required
def free(spot, day):
    form = BaseForm()
    if form.validate_on_submit():
        # TODO: Error handling and testing
        spot = ParkingSpot.query.filter_by(id=spot).first()
        if spot is None:
            flash(f"Spot {spot} not found.")
            return redirect(url_for("parking.index"))
        success = spot.free(day, current_user)
        if success:
            db.session.commit()
            flash(f"Spot {spot} is now free!")
        else:
            flash(f"Spot {spot} is not reserved by you.", "error")
        return redirect(url_for("parking.index"))
    else:
        return redirect(url_for("parking.index"))

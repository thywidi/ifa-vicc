from flask import render_template
from flask_login import login_required
from app.parking import bp
from app.parking.calendar import ParkingCalendar
import datetime

Calendar = ParkingCalendar()


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    year = datetime.date.today().year
    month = datetime.date.today().month
    return render_template(
        "pages/index.html",
        title="Home",
        year=year,
        month=month,
        today=datetime.date.today().day,
        weeks=Calendar.get_days(month),
    )

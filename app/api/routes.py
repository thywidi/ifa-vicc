from app.api import bp


@bp.route("/parking", methods=["GET", "POST"])
def parking():
    return "Parking"

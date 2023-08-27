from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reservations = db.relationship("Reservation", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"


class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    info = db.Column(db.String(256))
    reservations = db.relationship(
        "Reservation", backref="parking_spot", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Parkingspot {self.id}>"


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey("parking_spot.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Reservation {self.id}>"

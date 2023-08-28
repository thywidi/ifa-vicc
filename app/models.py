from app import db, login, logging
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reservations = db.relationship("Reservation", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    info = db.Column(db.String(256))
    reservations = db.relationship(
        "Reservation", backref="parking_spot", lazy="dynamic"
    )

    def is_reserved(self, date):
        return self.reservations.filter_by(date=date).first() is not None

    def reserve(self, date, user):
        if not self.is_reserved(date):
            self.reservations.append(Reservation(date=date, user=user))

    def free(self, date, user):
        userHasReservation = self.reservations.filter_by(date=date, user=user).first()
        if userHasReservation:
            self.reservations.remove(userHasReservation)
            return True
        else:
            return False

    def __repr__(self):
        return f"<Parkingspot {self.id}>"


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey("parking_spot.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Reservation {self.id}>"

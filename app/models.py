import base64
import os
from datetime import datetime, timedelta
from flask import url_for
from app import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class CollectionMixin(object):
    @staticmethod
    def to_collection_dict(query):
        resources = query.all()
        data = {
            "items": [item.to_dict() for item in resources],
        }
        return data


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reservations = db.relationship("Reservation", backref="user", lazy="dynamic")
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def reservation(self, date):
        return self.reservations.filter_by(date=date).first()

    def __repr__(self):
        return f"<User {self.username}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class ParkingSpot(db.Model, CollectionMixin):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    info = db.Column(db.String(256))
    reservations = db.relationship(
        "Reservation", backref="parking_spot", lazy="dynamic"
    )

    def is_reserved(self, date):
        return self.reservations.filter_by(date=date).first()

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

    def to_dict(self):
        data = {
            "id": self.id,
            "price": self.price,
            "info": self.info,
            "reservation_count": self.reservations.count(),
            "_links": {
                "self": url_for("api.get_spot", id=self.id),
                "reservations": url_for("api.get_spot_reservations", id=self.id),
                "reserved": url_for("api.get_spot_reserved", id=self.id),
            },
        }
        return data

    def __repr__(self):
        return f"<Parkingspot {self.id}>"


class Reservation(db.Model, CollectionMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey("parking_spot.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        data = {
            "id": self.id,
            "date": self.date,
            "parking_spot_id": self.parking_spot_id,
            "user_id": self.user_id,
            "_links": {
                "self": url_for("api.get_reservation", id=self.id),
                "user": url_for("api.get_reservation_user", id=self.id),
                "spot": url_for("api.get_reservation_spot", id=self.id),
            },
        }
        return data

    def __repr__(self):
        return f"<Reservation {self.id}>"

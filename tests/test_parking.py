import datetime

from app.models import Reservation, User, ParkingSpot
import pytest
from app import create_app, db
from tests.testconf import TestConfig
from flask_login import FlaskLoginClient


@pytest.fixture
def testApp():
    app = create_app(TestConfig)
    app.test_client_class = FlaskLoginClient
    with app.app_context():
        db.create_all()
        # Create default parking spots
        for x in range(1, 4):
            spot = ParkingSpot(id=x, price=5, info=f"Spot {x}")
            db.session.add(spot)
        db.session.commit()

        u = User(username="susan")  # type: ignore
        u.set_password("cat")
        db.session.add(u)
        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(testApp):
    user = User.query.filter_by(username="susan").first()
    return testApp.test_client(user=user)


class TestParking:
    def test_reserve_model(self, testApp):  # noqa: F811
        today = datetime.date.today()
        spot = ParkingSpot.query.filter_by(id=1).first()
        spot.reserve(today, User.query.filter_by(username="susan").first())
        assert spot.is_reserved(today)

    def test_free_model(self, testApp):  # noqa: F811
        today = datetime.date.today()
        spot = ParkingSpot.query.filter_by(id=1).first()
        spot.reserve(today, User.query.filter_by(username="susan").first())
        userReservation = spot.free(
            today, User.query.filter_by(username="susan").first()
        )
        # User should have a reservation which will be cleared
        assert userReservation is not None

    def test_reserve_route(self, client, testApp):
        today = datetime.date.today()
        with client:
            response = client.post(f"/reserve/1/{today.isoformat()}")
        assert response.status_code == 302
        with testApp.app_context():
            assert Reservation.query.filter_by(date=today).first() is not None

    def test_free_route(self, client, testApp):
        today = datetime.date.today()
        with client:
            response = client.post(f"/reserve/1/{today.isoformat()}")
            response = client.post(f"/free/1/{today.isoformat()}")
        assert response.status_code == 302
        with testApp.app_context():
            assert Reservation.query.filter_by(date=today).first() is None

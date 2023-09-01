import datetime

from sqlalchemy import select
from app.models import User, ParkingSpot, Reservation
import pytest
from app import create_app, db
from tests.testconf import TestConfig


@pytest.fixture
def accountingFixture():
    app = create_app(TestConfig)
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

        today = datetime.date.today()
        r = Reservation(user_id=u.id, parking_spot_id=1, date=today)
        db.session.add(r)
        db.session.commit()

        tomorrow = today + datetime.timedelta(days=1)
        r2 = Reservation(user_id=u.id, parking_spot_id=2, date=tomorrow)
        db.session.add(r2)
        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()


class TestAccounting:
    @pytest.mark.dependency()
    def test_spot_count(self, accountingFixture):  # noqa: F811
        """There should be 3 parking spots with the given fixture"""
        spots = db.session.scalars(select(ParkingSpot)).all()
        spotCount = len(list(spots))

        assert spotCount == 3

    @pytest.mark.dependency()
    def test_no_future_reservations(self, accountingFixture):  # noqa: F811
        """Future reservations should not be counted in accounting"""
        today = datetime.date.today()
        reservations = db.session.scalars(
            select(Reservation)
            .filter(Reservation.date <= today)
            .join(ParkingSpot)
            .join(User)
        ).all()
        assert len(reservations) == 1

    @pytest.mark.dependency(
        depends=[
            "TestAccounting::test_spot_count",
            "TestAccounting::test_no_future_reservations",
        ]
    )
    def test_occupied(self, accountingFixture):  # noqa: F811
        """Test accounting calculations"""
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
        assert occupied == 1
        assert occupation == 33.33
        assert revenue == 5

from app.models import User
import pytest
from tests.testconf import TestConfig  # noqa: F401
from app import create_app, db


@pytest.fixture
def testApp():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(testApp):
    return testApp.test_client()


class TestUser:
    @pytest.mark.dependency()
    def test_password_hashing(self, testApp):  # noqa: F811
        u = User(username="susan")  # type: ignore
        u.set_password("cat")
        assert not u.check_password("dog")
        assert u.check_password("cat")

    @pytest.mark.dependency(depends=["TestUser::test_password_hashing"])
    def test_required_form(self, client, testApp):
        response = client.post(
            "/auth/register", data={"username": "flask", "password": "cat"}
        )
        assert response.status_code == 200
        assert b"required" in response.data

        with testApp.app_context():
            assert User.query.filter_by(username="flask").first() is None

        response = client.post(
            "/auth/register",
            data={
                "username": "flask",
                "password": "cat",
                "passwordRepeat": "cat",
                "email": "test@test.com",
            },
        )
        assert response.status_code == 302
        assert b"login" in response.data
        with testApp.app_context():
            assert User.query.filter_by(username="flask").first() is not None

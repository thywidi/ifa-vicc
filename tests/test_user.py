from app.models import User
from tests.dbfixture import fixture  # noqa: F401


class TestClass:
    def test_password_hashing(self, fixture):  # noqa: F811
        u = User(username="susan")  # type: ignore
        u.set_password("cat")
        assert not u.check_password("dog")


from flask.testing import FlaskClient

from src.models import User_account, db
from tests.utils import refresh_db


def test_user_not_in_session(test_app: FlaskClient):
    refresh_db()
    
    res = test_app.get('/')
    page_data: str = res.data.decode()

    assert f'<a class="nav-link text-light" href="/login_page">Login/Register</a>' in page_data

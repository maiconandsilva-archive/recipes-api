import pytest
import wsgi


@pytest.fixture
def client():
    """Flask application context and database initialization."""

    app = wsgi.create_app()
    app.config['TESTING'] = True

    with app.test_client() as client_ctx:
        with app.app_context():
            wsgi.init_db()
        yield client_ctx

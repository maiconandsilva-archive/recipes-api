import pytest
import wsgi


app = wsgi.create_app()
app.testing = True

with app.app_context():
    wsgi.init_db()

with app.test_client() as client_ctx:
    @pytest.fixture
    def client():
        """Flask application context and database initialization."""
        yield client_ctx

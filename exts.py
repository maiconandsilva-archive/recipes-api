from flask_wtf.csrf import CSRFProtect

from db import SQLAlchemy


db = SQLAlchemy()
csrf = CSRFProtect()

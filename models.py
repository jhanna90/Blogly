"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User(db.Model):
    """Blog User"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default="DEFAULT_IMAGE_URL")

    @property
    def full_name(self):
        """Returns User's name."""

        return f"{self.first_name} {self.last_name}"


def connect_db(app):
    """Connects database to Flask app."""

    db.app = app
    db.init_app(app)

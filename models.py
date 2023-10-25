"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
     """User model"""

     __tablename__ = "users"

     id = db.Column(db.Integer, primary_key=True)
     first_name = db.Column(db.Text, nullable=False)
     last_name = db.Column(db.Text, nullable=False)
     image_url = db.Column(db.Text, nullable=False, default="https://img.freepik.com/premium-vector/accoun-vector-icon-with-long-shadow-white-illustration-isolated-blue-round-background-graphic-web-design_549897-771.jpg")


def connect_db(app):
     """Connect this database to the given Flask app."""
     
     db.app = app
     db.init_app(app)
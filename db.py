from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.testing.pickleable import User

from config import Config
import pymysql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+pymysql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}/timetable'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    schedule = db.Column(db.JSON)

    def __init__(self, name, schedule=None):
        self.name = name
        self.schedule = schedule or {}

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def find_by_name(name) -> 'User':
        return User.query.filter_by(name=name).first()

    @staticmethod
    def create_user(name) -> User:
        user = User(name)
        db.session.add(user)
        db.session.commit()
        return user

    def update_schedule(self, schedule):
        self.schedule = schedule
        db.session.commit()


def init_db():
    with app.app_context():
        db.create_all()
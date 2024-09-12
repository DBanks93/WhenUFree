from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy

from config import Timetable, Config

# from db import app, db, User, init_db

# app = Flask(__name__)


app = Flask(__name__)

app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(days=30)

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
    def find_by_name(name) -> 'User':
        return User.query.filter_by(name=name).first()

    @staticmethod
    def create_user(name):
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

init_db()

@app.route("/timetable")
def timetable():
    return redirect(url_for("login"))

@app.route("/timetable/login", methods=['GET'])
def login():
    if 'name' in session:
        return redirect(url_for('schedule'))
    return render_template('login.html')

@app.route("/timetable/login", methods=['POST'])
def post_login():
    name = request.form['name']
    session['name'] = name
    user = User.find_by_name(name)

    if not user:
        User.create_user(name)

    return redirect(url_for('schedule'))


@app.route("/timetable/schedule")
def schedule():
    if 'name' not in session:
        return redirect(url_for('login'))

    name = session['name']
    user = User.find_by_name(name)

    return render_template(
        'schedule.html',
        days= Timetable.DAYS,
        times=Timetable.TIMES,
        schedule=user.schedule or {})

@app.route("/timetable/schedule", methods=['POST'])
def save_schedule():
    if 'name' not in session:
        return redirect(url_for('login'))

    name = session['name']
    user = User.find_by_name(name)

    if not user:
        return jsonify({'error': 'User not logged in'}), 401

    schedule_data = request.json
    if not schedule_data:
        return jsonify({'error': 'schedule data missing'}), 400

    user.update_schedule(schedule_data)

    return jsonify({'message': "Schedule updated"})

@app.route("/logout")
def logout():
    session.pop('name')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
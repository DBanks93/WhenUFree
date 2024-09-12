from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from datetime import timedelta

from config import Timetable, Config
from db import app, db, User, init_db
from timetable_generator import TimetableGenerator, remove_working_times

# app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(days=30)

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

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/timetable/generate")
def generate_timetable():
    freshers_fair_slots = 4

    users = User.get_all_users()
    names = [user.name for user in users]

    people = {user.name: user.schedule for user in users}


    timetable_generator = TimetableGenerator(
        people,
        ['Wednesday', 'Thursday'],
        '10:00',
        '18:00',
        120,
        2,
        2
    )

    freshers_fair = timetable_generator.generate_timetable()
    people = remove_working_times(people, freshers_fair, 120)

    timetable_generator = TimetableGenerator(
        people,
        Timetable.DAYS,
        '11:00',
        '15:00',
        120,
        2,
        2
    )
    leafleting = timetable_generator.generate_timetable()

    timetable_result = {
        'freshers_fair': freshers_fair,
        'leafleting': leafleting
    }

    return jsonify(timetable_result), 200

@app.route('/timetable/people')
def people():
    users = User.get_all_users()

    return render_template(
        'people.html',
        people=users)

if __name__ == "__main__":
    app.run(debug=True)
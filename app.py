from flask import Flask, render_template, request, redirect, url_for, flash
import sys
import requests
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config.update(SECRET_KEY=os.urandom(5))


class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)


db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    city_list = City.query.all()
    weather_info = []
    for city in city_list:
        w = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid=430243c500502c9dcb2939f552371a49").json()
        w['id'] = city.id
        weather_info.append(w)

    return render_template('index.html', weather=weather_info)


@app.route('/add', methods=['POST', 'GET'])
def add():
    city = request.form.get('city_name')
    try:
        if City.query.filter(City.name == city).first():
            flash("The city has already been added to the list!")
        elif requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=430243c500502c9dcb2939f552371a49").json()['cod'] == '404':
            flash("The city doesn't exist!")
        else:
            db.session.add(City(name=city))
            db.session.commit()
    except Exception as error:
        flash("The city doesn't exist!")
    return redirect(url_for('index'))


@app.route('/delete/<city_id>', methods=['POST', 'GET'])
def delete(city_id):
    try:
        db.session.delete(City.query.filter(City.id == city_id).first())
        db.session.commit()
    except Exception:
        pass
    return redirect(url_for('index'))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()


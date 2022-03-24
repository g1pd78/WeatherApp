from flask import Flask, render_template, request, redirect, url_for
import sys
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'


class NonExistentСity(Exception):
    pass


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
        try:
            w = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid=430243c500502c9dcb2939f552371a49").json()
            weather_info.append(w)
        except NonExistentСity:
            pass
    return render_template('index.html', weather=weather_info)


@app.route('/add', methods=['POST', 'GET'])
def add():
    city = request.form.get('city_name')
    if city:
        db.session.add(City(name=city))
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()


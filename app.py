from flask import Flask, render_template, request
import sys
import requests

app = Flask(__name__)


#@app.route('/', methods=['POST', 'GET'])
#def index():
#    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
def add():
    city = request.form.get('city_name')
    if city:
        weather_info = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=430243c500502c9dcb2939f552371a49")
        return render_template('index.html', weather=weather_info.json())
    else:
        return render_template('index.html')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()

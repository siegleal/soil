from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for
from soil import Soil
import db
from datetime import datetime, timedelta

app = Flask(__name__)
soil = Soil()

@app.route('/')
def redirect_default():
  return redirect(url_for('index', plant='bendy_boi'))

@app.route('/index/<plant>')
def index(plant):
  return render_template('index.html', plant=plant, plant_names=db.get_plant_names())


@app.route('/static/<path:path>')
def send_js(path):
  return send_from_directory('static', path)


@app.route('/read')
def touch_and_temp():
    touch, temp = soil.read()
    return jsonify({'temp': temp, 'moisture': touch})

@app.route('/plantnames')
def get_plant_names():
    names = db.get_plant_names()
    return jsonify(names)

@app.route('/plant/<plant>/last24hours')
def read_plant_last_24_hours(plant: str):
  return db.get_last_24hours(plant)
  

@app.route('/plant')
def read_plant():
  plant_name = request.args.get('name', None)
  limit = request.args.get('limit', None)
  rows = db.read_plant(plant_name, limit)
  return jsonify({"num_values": len(rows), "values": [{"temp": r[0], "moisture": r[1], "plant": r[2], "timestamp": r[3]} for r in rows]})

@app.route('/moisturesma/<plant>')
def get_moisture_sma(plant: str):
  result = db.get_moisture_sma(plant)
  return jsonify({'values': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



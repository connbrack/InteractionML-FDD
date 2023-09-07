from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_from_directory
from flask_login import login_required, current_user
from .models import Defaults
from . import db
import pandas as pd
import json

data = Blueprint('data', __name__)


@data.route('/defaults', methods=['GET'])
def defaults():

    df = pd.read_sql_query('SELECT * FROM defaults', db.engine, index_col=None)
    output = df.to_dict(orient='index')[0]

    return jsonify(output)

@data.route('/AHU_sensor_info', methods=['GET'])
def sensor_info():

    df = pd.read_sql_query('SELECT * FROM AHU_info', db.engine, index_col=None)
    df = df.sort_values('num').set_index('num')
    output = df.to_dict(orient='index')

    return jsonify(output)


@data.route('/sensor_data', methods=['GET'])
def sensor_data():  

    plot_sensor = request.args.get('sensor')

    df = pd.read_sql_query('SELECT * FROM AHU_info', db.engine)
    sensor_info = df[df['label'] == plot_sensor]

    df = pd.read_sql_query('SELECT * FROM AHU_data', db.engine, parse_dates=['index'])
    df['index'] = (df['index'].astype(int) / 1000000).astype(int)
    df = df.set_index('index')
    df_plot = df[plot_sensor]
    data = [[k,v] for k,v in df_plot.items()]

    output = {
        'label': plot_sensor, 
        'name': sensor_info['name'].to_list()[0], 
        'unit': sensor_info['unit'].to_list()[0], 
        'data': data}

    return jsonify(output)


@data.route('/change_sensor', methods=['POST'])
def change_sensor():  
    post_data = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    plot_sensor = post_data['sensor']
    if plot_sensor:
        default = Defaults.query.filter_by(user_id=1).first()
        default.view_sensor = plot_sensor
        db.session.commit()

    return jsonify({})


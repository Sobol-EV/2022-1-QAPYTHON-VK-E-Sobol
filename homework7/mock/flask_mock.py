#!/usr/bin/env python3.9
import json
import threading

from flask import Flask, jsonify, request

import settings

app = Flask(__name__)

ID_DATA = {}
APP_DATA = {}
LAST_NAME_DATA = {}


@app.route('/add_user', methods=['POST'])
def create_user():
    user_name = json.loads(request.data)['first_name']
    if user_name not in APP_DATA:
        APP_DATA[user_name] = ID_DATA[user_name]
        return jsonify({'user_id': APP_DATA[user_name]}), 201
    else:
        return jsonify(
            f'User_name {user_name} already exists: id: {APP_DATA[user_name]}'
        ), 400


@app.route('/get_user/<name>', methods=['GET'])
def get_user(name):
    if user_id := APP_DATA.get(name):
        if last_name := LAST_NAME_DATA.get(name):
            user_data = {
                'user_id': user_id,
                'first_name': name,
                'last_name': last_name,
                }
            return jsonify(user_data), 200
        else:
            return jsonify(f'Last name for username {name} not found'), 404
    else:
        return jsonify(f'Username {name} not found'), 404


@app.route('/change_last_name_by_name/<name>', methods=['PUT'])
def change_user_last_name(name):
    new_last_name = json.loads(request.data)['new_last_name']
    if user_id := APP_DATA.get(name):
        if last_name := LAST_NAME_DATA.get(name):
            LAST_NAME_DATA[name] = new_last_name
            user_data = {
                'user_id': user_id,
                'first_name': name,
                'last_name': LAST_NAME_DATA[name],
            }
            return jsonify(user_data), 200
        else:
            return jsonify(f'Last name for username {name} not found'), 404
    else:
        return jsonify(f'Username {name} not found'), 404


@app.route('/delete_user_by_name/<name>', methods=['DELETE'])
def delete_user(name):
    if name in APP_DATA:
        if name in LAST_NAME_DATA:
            del LAST_NAME_DATA[name]
        del APP_DATA[name]
        return jsonify(APP_DATA), 201
    else:
        return jsonify(f'Username {name} not found'), 404


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_stub()

    return jsonify(f'Ok, exiting'), 200


def run_mock():
    server = threading.Thread(
        target=app.run,
        kwargs={
            'host': settings.MOCK_HOST,
            'port': settings.MOCK_PORT
        }
    )
    server.start()

    return server

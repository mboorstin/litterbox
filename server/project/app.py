import datetime
import json
import base64
import struct

from flask import Flask, abort, escape, jsonify, make_response, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

from models import Debug, Stall, Visit, Base
from XBeeParser import sender_and_status

SECRET = '1234567890'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///sqlite.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1.0/stalls', methods=['GET'])
def get_stalls():
    session = db.session()
    stalls = session.query(Stall).all()
    values = [stall.to_json() for stall in stalls]
    response = make_response()
    response.data = json.dumps(values)
    return response

@app.route('/api/v1.0/stalls', methods=['POST'])
def update_stalls():
    required = ['secret', 'stall_id', 'status']
    if not request.json or any(x not in request.json for x in required):
        abort(400)
    if request.json['secret'] != SECRET:
        abort(400)

    session = db.session()
    stall = session.query(Stall).get(request.json['stall_id'])
    if not stall:
        abort(400)
    if stall.status and not request.json['status']:
        print stall.visits.order_by(Visit.id.desc()).first().id
        stall.visits.order_by(Visit.id.desc()).first().exited_at = datetime.datetime.now()
        stall.status = request.json['status']
        session.commit()
    elif not stall.status and request.json['status']:
        session.add(Visit(stall_id=stall.id))
        stall.status = request.json['status']
        session.commit()
    return jsonify({'success': True}), 201

# raw_data is base64ified
# Doing JSON even for a single parameter to make life easier for later
@app.route('/api/v1.5/stalls', methods=['POST'])
def update_stalls_from_raw():
    required = ['raw_data']
    if not request.json or any(x not in request.json for x in required):
        abort(400)

    message_str = base64.b64decode(request.json['raw_data'])
    message_bytes = bytearray()
    message_bytes.extend(message_str)
    sender, status = sender_and_status(message_bytes)
    stall_id = struct.unpack('>I', sender[4:])[0]
    # We're using pull up resistors on the XBee's
    status = not status

    session = db.session()
    stall = session.query(Stall).get(stall_id)
    if not stall:
        abort(400)
    if stall.status and not status:
        print stall.visits.order_by(Visit.id.desc()).first().id
        stall.visits.order_by(Visit.id.desc()).first().exited_at = datetime.datetime.now()
        stall.status = False
        session.commit()
    elif not stall.status and status:
        session.add(Visit(stall_id=stall_id))
        stall.status = True
        session.commit()
    return jsonify({'success': True}), 201

@app.route('/api/v1.0/stall/<stall_id>', methods=['GET'])
def get_visits(stall_id):
    try:
        stall_id = int(stall_id)
    except ValueError:
        abort(400)

    session = db.session()
    stall = session.query(Stall).get(stall_id)
    if not stall:
        abort(400)

    response = make_response()
    visits = stall.visits.order_by(Visit.id.desc()).all()
    values = [visit.to_json() for visit in visits]
    response.data = json.dumps(values)
    return response

@app.route('/api/v1.0/debug', methods=['GET'])
def get_debug():
    session = db.session()
    debugs = session.query(Debug).order_by(Debug.id.desc()).all()
    values = [str(escape(str(debug))) for debug in debugs]
    response = make_response()
    response.data = '<br>'.join(values)
    return response

@app.route('/api/v1.0/debug', methods=['POST'])
def update_debug():
    data = request.get_data(as_text=True)

    session = db.session()
    session.add(Debug(message=data))
    session.commit()

    return jsonify({'success': True}), 201

if __name__ == '__main__':
    app.run(debug=True)

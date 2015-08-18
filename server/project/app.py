import datetime
import json

from flask import Flask, abort, jsonify, make_response, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

from models import Stall, Visit, Base

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

if __name__ == '__main__':
    app.run(debug=True)

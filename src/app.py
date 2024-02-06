import os
import json
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, TodoModel
from flask import jsonify
from utils import APIException

app = Flask(__name__)

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)


@app.route('/todos', methods=['GET'])
def index():
    todos = TodoModel.query.all()
    all_todos = list(map(lambda x: x.serialize(), todos))
    return jsonify(all_todos), 200

@app.route('/addtodos', methods=['POST'])
def add_new_todo():
    request_body = request.get_json()
    todo_data = TodoModel(label=request_body['label'], done=request_body['done'])
    db.session.add(todo_data)
    db.session.commit()
    return jsonify(request_body), 200

@app.route('/update/<int:id>', methods=['PUT'])
def update_todos(id):
    request_body = request.get_json()
    todo = TodoModel.query.get(id)
    if todo is None:
        raise APIException('Id de tarea no existe', status_code=400)
    if "label" in request_body:
        todo.label = request_body['label']
    if "done" in request_body:
        todo.done = request_body['done']
    db.session.commit()
    return jsonify(request_body), 200

@app.route('/done/<int:id>', methods=['PUT'])
def done_todos(id):
    todo = TodoModel.query.get(id)
    if todo is None:
        raise APIException('Id de tarea no existe', status_code=400)
    todo.done = True
    db.session.commit()
    return jsonify({"msg": "Tarea actualizada"}), 200

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_todos(id):
    todo = TodoModel.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"msg": "Tarea borrada"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)
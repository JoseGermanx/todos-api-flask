import os
import json
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, TodoModel

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

todos = [
    { "label": "My first task", "done": False },
    { "label": "My second task", "done": False }
]

@app.route('/todos', methods=['GET'])
def index():
    todos = TodoModel.query.all()
    all_todos = list(map(lambda x: x.serialize(), todos))
    return jsonify(all_todos), 200

@app.route('/addtodos', methods=['POST'])
def add_new_todo():
    request_body = request.get_json()
    handle_diccionary_to_str = json.dumps(request_body)
    add_todo = json.loads(handle_diccionary_to_str)
    todos.append(add_todo)
    return jsonify(todos)

@app.route('/update/<int:position>', methods=['PUT'])
def update_todos(position):
    request_body = request.get_json()
    if "label" in request_body:
        todos[position]['label'] = request_body['label']
    if "done" in request_body:
        if request_body['done'] == True:
            todos[position]['done'] = True
        else:
            todos[position]['done'] = False
    return jsonify(todos)

@app.route('/delete/<int:position>', methods=['DELETE'])
def delete_todos(position):
    todos.pop(position)
    return jsonify(todos)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)
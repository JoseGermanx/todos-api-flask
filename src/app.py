import json
from flask import Flask, jsonify, request

app = Flask(__name__)

todos = [
    { "label": "My first task", "done": False },
    { "label": "My second task", "done": False }
]

@app.route('/todos', methods=['GET'])
def index():
    return jsonify(todos)

@app.route('/addtodos', methods=['POST'])
def add_new_todo():
    request_body = request.get_json()
    handle_diccionary_to_str = json.dumps(request_body)
    add_todo = json.loads(handle_diccionary_to_str)
    todos.append(add_todo)
    return jsonify(todos)

@app.route('/delete/<int:position>', methods=['DELETE'])
def delete_todos(position):
    todos.pop(position)
    return jsonify(todos)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)
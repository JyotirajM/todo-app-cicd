from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "todos.json"


def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todos", methods=["GET"])
def get_todos():
    return jsonify(load_todos())


@app.route("/api/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or not data.get("title", "").strip():
        return jsonify({"error": "Title is required"}), 400
    todos = load_todos()
    todo = {
        "id": int(datetime.now().timestamp() * 1000),
        "title": data["title"].strip(),
        "completed": False,
        "created_at": datetime.now().isoformat(),
    }
    todos.append(todo)
    save_todos(todos)
    return jsonify(todo), 201


@app.route("/api/todos/<int:todo_id>", methods=["PATCH"])
def update_todo(todo_id):
    todos = load_todos()
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if "completed" in data:
        todo["completed"] = data["completed"]
    if "title" in data:
        todo["title"] = data["title"].strip()
    save_todos(todos)
    return jsonify(todo)


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todos = load_todos()
    todos = [t for t in todos if t["id"] != todo_id]
    save_todos(todos)
    return jsonify({"success": True})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

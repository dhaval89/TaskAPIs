from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory storage
tasks = []
categories = ['Work', 'Personal', 'Shopping']
users = {
    "user": {
        "email": "user@example.com",
        "name": "John Doe",
        "dark_mode": False,
    }
}

# Task structure: {id, title, description, category, priority, due_date, is_completed}

# Helper function to get next task ID
def get_next_task_id():
    return len(tasks) + 1

# Routes

# Task CRUD
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = {
        "id": get_next_task_id(),
        "title": data["title"],
        "description": data.get("description", ""),
        "category": data["category"],
        "priority": data["priority"],  # Low, Medium, High
        "due_date": datetime.strptime(data["due_date"], "%Y-%m-%dT%H:%M:%S") if data.get("due_date") else None,
        "is_completed": False,
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.json
    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    task["category"] = data.get("category", task["category"])
    task["priority"] = data.get("priority", task["priority"])
    task["due_date"] = datetime.strptime(data["due_date"], "%Y-%m-%dT%H:%M:%S") if data.get("due_date") else task["due_date"]
    task["is_completed"] = data.get("is_completed", task["is_completed"])

    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted successfully"})

# Categories
@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(categories)

# Analytics
@app.route('/analytics', methods=['GET'])
def get_analytics():
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["is_completed"])
    overdue_tasks = sum(1 for task in tasks if task["due_date"] and task["due_date"] < datetime.now())
    stats = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "overdue_tasks": overdue_tasks,
    }
    return jsonify(stats)

# User settings
@app.route('/settings/dark-mode', methods=['PUT'])
def toggle_dark_mode():
    user = users.get("user")
    user["dark_mode"] = not user["dark_mode"]
    return jsonify(user)

# Push notifications (simulated)
@app.route('/notifications', methods=['GET'])
def check_due_tasks():
    now = datetime.now()
    due_soon = [task for task in tasks if task["due_date"] and now <= task["due_date"] <= now + timedelta(hours=1)]
    return jsonify({"due_soon": due_soon})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
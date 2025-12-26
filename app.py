from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import get_connection
import logging
def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()

app = Flask(__name__)

# Logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# -------------------- TEMPLATE ROUTES --------------------

@app.route("/")
def list_tasks():
    conn = get_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("tasks.html", tasks=tasks)

@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        try:
            title = request.form["title"]
            description = request.form["description"]
            due_date = request.form["due_date"]

            conn = get_connection()
            conn.execute(
                "INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)",
                (title, description, due_date)
            )
            conn.commit()
            conn.close()

            logging.info("Task added via UI")
            return redirect(url_for("list_tasks"))

        except Exception as e:
            logging.error(str(e))
            return "Error adding task", 500

    return render_template("add_task.html")

# -------------------- API ROUTES --------------------

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return jsonify([dict(task) for task in tasks]), 200

@app.route("/api/tasks", methods=["POST"])
def create_task():
    try:
        data = request.get_json(force=True)

        if not data or "title" not in data:
            return jsonify({"error": "Title is required"}), 400

        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)",
            (
                data["title"],
                data.get("description", ""),
                data.get("due_date", ""),
                data.get("status", "pending")
            )
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()

        return jsonify({"id": task_id, "message": "Task created"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(force=True)

    conn = get_connection()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id=?",
        (task_id,)
    ).fetchone()

    if not task:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    title = data.get("title", task["title"])
    description = data.get("description", task["description"])
    due_date = data.get("due_date", task["due_date"])
    status = data.get("status", task["status"])

    conn.execute(
        """
        UPDATE tasks
        SET title=?, description=?, due_date=?, status=?
        WHERE id=?
        """,
        (title, description, due_date, status, task_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Task updated"}), 200


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

    logging.info(f"Task {task_id} deleted")
    return jsonify({"message": "Task deleted"}), 200

init_db()


if __name__ == "__main__":
    app.run(debug=True)

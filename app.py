from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "lost_and_found.db"

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-key"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if not DB_PATH.exists():
        conn = get_db_connection()
        conn.execute(
            """
            CREATE TABLE reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT,
                email TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT,
                status TEXT NOT NULL DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        conn.close()


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/report", methods=["POST"])
def report_item():
    student_name = request.form.get("student_name", "").strip()
    email = request.form.get("email", "").strip()
    description = request.form.get("description", "").strip()
    location = request.form.get("location", "").strip()

    if not email or not description:
        flash("Email and item description are required.", "error")
        return redirect(url_for("index"))

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO reports (student_name, email, description, location) VALUES (?, ?, ?, ?)",
        (student_name, email, description, location),
    )
    conn.commit()
    conn.close()

    flash("Report submitted successfully. An admin will review it soon.", "success")
    return redirect(url_for("index"))


@app.route("/admin")
def admin_panel():
    conn = get_db_connection()
    reports = conn.execute("SELECT * FROM reports ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("admin.html", reports=reports)


@app.route("/resolve/<int:report_id>", methods=["POST"])
def resolve_report(report_id):
    conn = get_db_connection()
    conn.execute("UPDATE reports SET status = 'resolved' WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()
    flash("Report marked as resolved.", "success")
    return redirect(url_for("admin_panel"))


if __name__ == "__main__":
    app.run(debug=True)

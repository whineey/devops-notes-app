from flask import Flask, render_template, request, redirect, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

with app.app_context():
    init_db()

@app.route("/")
def index():
    filter_type = request.args.get("filter", "all")

    conn = get_connection()
    cur = conn.cursor()

    if filter_type == "active":
        cur.execute("""
            SELECT id, content, completed, created_at 
            FROM notes 
            WHERE completed = FALSE
            ORDER BY created_at DESC;
        """)
    elif filter_type == "completed":
        cur.execute("""
            SELECT id, content, completed, created_at 
            FROM notes 
            WHERE completed = TRUE
            ORDER BY created_at DESC;
        """)
    else:
        cur.execute("""
            SELECT id, content, completed, created_at 
            FROM notes 
            ORDER BY created_at DESC;
        """)

    notes = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("index.html", notes=notes, current_filter=filter_type)


@app.route("/add", methods=["POST"])
def add_note():
    content = request.form.get("content")
    if content:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (content) VALUES (%s);", (content,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect("/")

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/api/notes")
def api_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, content, created_at FROM notes;")
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(notes)

@app.route("/toggle/<int:note_id>", methods=["POST"])
def toggle_note(note_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE notes
        SET completed = NOT completed
        WHERE id = %s;
    """, (note_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s;", (note_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

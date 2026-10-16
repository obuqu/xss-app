from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecret-demo-key"

DB = "data/vuln.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

# --- REFLECTED XSS (уязвимо) ---
@app.route("/search")
def search():
    q = request.args.get("q", "")
    return render_template("search.html", query=q)

# --- STORED XSS (уязвимо) ---
@app.route("/comments", methods=["GET", "POST"])
def comments():
    if request.method == "POST":
        author = request.form.get("author", "Anonymous")
        text = request.form.get("text", "")
        conn = sqlite3.connect(DB)
        conn.execute("INSERT INTO comments (author, text) VALUES (?, ?)", (author, text))
        conn.commit()
        conn.close()
        return redirect(url_for("comments"))

    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT id, author, text FROM comments ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("comments.html", comments=rows)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
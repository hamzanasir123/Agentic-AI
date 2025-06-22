from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def dashboard():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT name, role, company, email, status, timestamp, email_preview FROM outreach_logs ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()
    return render_template("dashboard.html", logs=logs)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coffee(
        id INTEGER PRIMARY KEY,
        name TEXT,
        votes INTEGER
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM coffee")
    count = cursor.fetchone()[0]

    if count == 0:
        coffees = [
            (1, "Espresso", 0),
            (2, "Cappuccino", 0),
            (3, "Latte", 0)
        ]
        cursor.executemany("INSERT INTO coffee VALUES (?, ?, ?)", coffees)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/coffee")
def get_coffee():
    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM coffee")
    data = cursor.fetchall()

    conn.close()

    coffees = []

    for row in data:
        coffees.append({
            "id": row[0],
            "name": row[1],
            "votes": row[2]
        })

    return jsonify(coffees)

@app.route("/vote", methods=["POST"])
def vote():
    data = request.json

    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE coffee SET votes = votes + 1 WHERE id=?",
        (data["id"],)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Vote Added"})

if __name__ == "__main__":
    app.run(debug=True)
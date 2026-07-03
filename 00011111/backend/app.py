from flask import Flask, request, jsonify
import sqlite3
import jwt
import datetime

app = Flask(__name__)

DB = "database.db"
SECRET = "supersecretkey"


# ---------------- DB INIT ----------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        """
    CREATE TABLE IF NOT EXISTS students (
        roll TEXT PRIMARY KEY,
        name TEXT,
        mar INT, eng INT, mat INT,
        es1 INT, arts INT, prac INT, pe INT,
        percentage REAL,
        grade TEXT
    )
    """
    )

    c.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """
    )

    # Default admin
    c.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'admin123')")

    conn.commit()
    conn.close()


init_db()


# ---------------- GRADE ----------------
def get_grade(p):
    if p >= 91:
        return "A1"
    elif p >= 81:
        return "A2"
    elif p >= 71:
        return "B1"
    elif p >= 61:
        return "B2"
    elif p >= 51:
        return "C1"
    elif p >= 41:
        return "C2"
    elif p >= 31:
        return "D"
    elif p >= 21:
        return "E1"
    else:
        return "E2"


# ---------------- LOGIN ----------------
@app.route("/")
def home():
    return "Student Management API is running 🚀"


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"]),
    )

    user = c.fetchone()
    conn.close()

    if user:
        token = jwt.encode(
            {
                "user": data["username"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            },
            SECRET,
            algorithm="HS256",
        )

        return jsonify({"success": True, "token": token})

    return jsonify({"success": False, "error": "Invalid "}), 401


# ---------------- ADD STUDENT ----------------
@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.json

    marks = [data[x] for x in ["mar", "eng", "mat", "es1", "arts", "prac", "pe"]]
    percentage = sum(marks) / len(marks)
    grade = get_grade(percentage)

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    try:
        c.execute(
            """
        INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """,
            (
                data["roll"],
                data["name"],
                data["mar"],
                data["eng"],
                data["mat"],
                data["es1"],
                data["arts"],
                data["prac"],
                data["pe"],
                percentage,
                grade,
            ),
        )

        conn.commit()
        return jsonify({"message": "Student added"})
    except:
        return jsonify({"error": "Roll number exists"})
    finally:
        conn.close()


# ---------------- GET STUDENTS ----------------
@app.route("/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect(DB)
    df = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return jsonify(df)


# ---------------- UPDATE ----------------
@app.route("/update_student", methods=["PUT"])
def update_student():
    data = request.json

    marks = [data[x] for x in ["mar", "eng", "mat", "es1", "arts", "prac", "pe"]]
    percentage = sum(marks) / len(marks)
    grade = get_grade(percentage)

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        """
    UPDATE students SET name=?, mar=?, eng=?, mat=?, es1=?, arts=?, prac=?, pe=?, percentage=?, grade=?
    WHERE roll=?
    """,
        (
            data["name"],
            data["mar"],
            data["eng"],
            data["mat"],
            data["es1"],
            data["arts"],
            data["prac"],
            data["pe"],
            percentage,
            grade,
            data["roll"],
        ),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Updated successfully"})


# ---------------- DELETE ----------------
@app.route("/delete_student/<roll>", methods=["DELETE"])
def delete_student(roll):
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM students WHERE roll=?", (roll,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted"})


if __name__ == "__main__":
    app.run(debug=True)

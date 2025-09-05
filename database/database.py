from flask import Flask, request, redirect, url_for
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Path for the database
DB_PATH = Path(__file__).resolve().parent / "diabetes.db"


# -------- Database setup --------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        emailid VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """)

    # Diabetes table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Diabetes (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        Pregnancies INTEGER CHECK (Pregnancies >= 0),
        Glucose INTEGER CHECK (Glucose > 0),
        BloodPressure INTEGER CHECK (BloodPressure >= 0),
        SkinThickness INTEGER CHECK (SkinThickness >= 0),
        Insulin INTEGER CHECK (Insulin >= 0),
        BMI DECIMAL(5,2) CHECK (BMI > 0),
        DiabetesPedigreeFunction DECIMAL(5,3) CHECK (DiabetesPedigreeFunction > 0),
        Age INTEGER CHECK (Age > 0),
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Database ready!")


# -------- LOGIN route --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM Users WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            return redirect(url_for("form", user_id=user[0]))
        else:
            return {"message": "❌ Invalid username or password"}

    # GET request
    return {"message": "Submit username & password via POST"}


# -------- FORM route --------
@app.route('/form/<int:user_id>', methods=['GET', 'POST'])
def form(user_id):
    if request.method == "POST":
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Get diabetes inputs
        Pregnancies = int(request.form.get("Pregnancies"))
        Glucose = int(request.form.get("Glucose"))
        BloodPressure = int(request.form.get("BloodPressure"))
        SkinThickness = int(request.form.get("SkinThickness"))
        Insulin = int(request.form.get("Insulin"))
        BMI = float(request.form.get("BMI"))
        DiabetesPedigreeFunction = float(request.form.get("DiabetesPedigreeFunction"))
        Age = int(request.form.get("Age"))

        # Insert into Diabetes
        cur.execute("""
        INSERT INTO Diabetes (user_id, Pregnancies, Glucose, BloodPressure, SkinThickness,
                              Insulin, BMI, DiabetesPedigreeFunction, Age)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, Pregnancies, Glucose, BloodPressure, SkinThickness,
              Insulin, BMI, DiabetesPedigreeFunction, Age))

        conn.commit()
        conn.close()

        return {"message": f"✅ Diabetes record added for user_id {user_id}"}

    # GET request (just opening in browser)
    return {"message": f"Form ready for user_id {user_id}, send data via POST"}


if __name__ == "__main__":
    init_db()
    app.run(debug=True)



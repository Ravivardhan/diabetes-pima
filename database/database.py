import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "diabetes.db"

def ensure_tables():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        emailid VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """)

    # Diabetes
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
        CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES Users(user_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at: {DB_PATH}")

if __name__ == "__main__":
    ensure_tables()

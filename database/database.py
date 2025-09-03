import sqlite3
from pathlib import Path

 database-work
# Path for the database file
DB_PATH = Path(__file__).resolve().parent / "diabetes.db"

def init_db():
    """Initialize the Users and Diabetes tables"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
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

        print("✅ Database initialized successfully.")

def insert_user(username, email, password):
    """Insert a new user (skip if exists)"""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM Users WHERE emailid = ?", (email,))
        user = cur.fetchone()

        if user:
            print(f"⚠️ User with email {email} already exists.")
            return user[0]
        else:
            cur.execute("INSERT INTO Users (username, emailid, password) VALUES (?, ?, ?)",
                        (username, email, password))
            print(f"✅ User {username} inserted.")
            return cur.lastrowid

def insert_diabetes_record(user_id, Pregnancies, Glucose, BloodPressure, SkinThickness,
                           Insulin, BMI, DiabetesPedigreeFunction, Age):
    """Insert a diabetes record for a given user"""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO Diabetes (user_id, Pregnancies, Glucose, BloodPressure, SkinThickness,
                              Insulin, BMI, DiabetesPedigreeFunction, Age)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, Pregnancies, Glucose, BloodPressure, SkinThickness,
              Insulin, BMI, DiabetesPedigreeFunction, Age))
        print(f"✅ Diabetes record added for user_id {user_id}.")

def get_all_users():
    """Fetch all users"""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users")
        return cur.fetchall()

def get_user_records(username):
    """Fetch diabetes records for a user by username"""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
        SELECT D.* FROM Diabetes D
        JOIN Users U ON U.user_id = D.user_id
        WHERE U.username = ?
        """, (username,))
        return cur.fetchall()

if __name__ == "__main__":
    # Initialize DB
    init_db()

    # Example inserts
    uid = insert_user("vasu", "vasu@example.com", "hashed_pw_123")
    insert_diabetes_record(uid, 2, 120, 70, 20, 80, 25.5, 0.75, 30)

    # Fetch data
    print("👥 Users:", get_all_users())
    print("📊 Vasu's records:", get_user_records("vasu"))


=======
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

import sqlite3
from datetime import datetime

DB_NAME = "bookings.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            booking_type TEXT,
            date TEXT,
            time TEXT,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        )
    """)

    conn.commit()
    conn.close()

def save_booking(booking):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
        (booking["name"], booking["email"], booking["phone"])
    )

    customer_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO bookings 
        (customer_id, booking_type, date, time, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            customer_id,
            booking["booking_type"],
            booking["date"],
            booking["time"],
            "CONFIRMED",
            datetime.now().isoformat()
        )
    )

    booking_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return booking_id

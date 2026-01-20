import streamlit as st
import sqlite3
import pandas as pd

DB_NAME = "bookings.db"

def get_all_bookings():
    conn = sqlite3.connect(DB_NAME)
    query = """
    SELECT 
        b.id AS booking_id,
        c.name,
        c.email,
        c.phone,
        b.booking_type,
        b.date,
        b.time,
        b.status,
        b.created_at
    FROM bookings b
    JOIN customers c ON b.customer_id = c.customer_id
    ORDER BY b.created_at DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.set_page_config(page_title="Admin Dashboard", page_icon="📊")

st.title("📊 Admin Dashboard – Doctor Appointments")

df = get_all_bookings()

if df.empty:
    st.info("No bookings available.")
else:
    st.dataframe(df, use_container_width=True)

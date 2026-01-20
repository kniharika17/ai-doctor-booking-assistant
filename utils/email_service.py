import smtplib
from email.message import EmailMessage
import streamlit as st
import traceback

def send_confirmation_email(to_email, booking_id, booking):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Doctor Appointment Confirmation"
        msg["From"] = st.secrets["EMAIL_USER"]
        msg["To"] = to_email

        msg.set_content(f"""
Hello {booking['name']},

Your appointment has been confirmed successfully.

Booking ID: {booking_id}
Consultation Type: {booking['booking_type']}
Date: {booking['date']}
Time: {booking['time']}

Thank you for choosing our clinic.
""")

        smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp.login(
            st.secrets["EMAIL_USER"],
            st.secrets["EMAIL_PASSWORD"]
        )
        smtp.send_message(msg)
        smtp.quit()

        return True

    except Exception as e:
        print("EMAIL ERROR:", e)
        traceback.print_exc()
        return False

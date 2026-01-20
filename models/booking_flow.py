import re
from datetime import datetime

REQUIRED_FIELDS = [
    "name",
    "email",
    "phone",
    "booking_type",
    "date",
    "time"
]

QUESTIONS = {
    "name": "May I know your **full name**?",
    "email": "Please provide your **email address**.",
    "phone": "Please provide your **phone number**.",
    "booking_type": "What type of consultation do you need? (e.g., General / Specialist)",
    "date": "Preferred **appointment date**? (YYYY-MM-DD)",
    "time": "Preferred **appointment time**? (HH:MM)"
}

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_time(time_str):
    return re.match(r"^\d{2}:\d{2}$", time_str)


def initialize_booking_state(session_state):
    if "booking" not in session_state:
        session_state.booking = {field: None for field in REQUIRED_FIELDS}
        session_state.booking["confirmed"] = False

def get_next_question(booking):
    for field in REQUIRED_FIELDS:
        if booking[field] is None:
            return QUESTIONS[field]
    return None

def update_booking_state(booking, user_input):
    if booking["name"] is None:
        booking["name"] = user_input
        return None

    if booking["email"] is None:
        if is_valid_email(user_input):
            booking["email"] = user_input
            return None
        return "❌ Please enter a valid email address (e.g., name@gmail.com)."

    if booking["phone"] is None:
        if is_valid_phone(user_input):
            booking["phone"] = user_input
            return None
        return "❌ Phone number must contain exactly 10 digits."

    if booking["booking_type"] is None:
        booking["booking_type"] = user_input
        return None

    if booking["date"] is None:
        if is_valid_date(user_input):
            booking["date"] = user_input
            return None
        return "❌ Please enter date in YYYY-MM-DD format."

    if booking["time"] is None:
        if is_valid_time(user_input):
            booking["time"] = user_input
            return None
        return "❌ Please enter time in HH:MM format."


def summarize_booking(booking):
    return f"""
### 🩺 Appointment Summary

- **Name:** {booking['name']}
- **Email:** {booking['email']}
- **Phone:** {booking['phone']}
- **Consultation Type:** {booking['booking_type']}
- **Date:** {booking['date']}
- **Time:** {booking['time']}

✅ Please confirm: **Yes / No**
"""

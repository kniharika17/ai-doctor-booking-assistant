import re

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
    elif booking["email"] is None and "@" in user_input:
        booking["email"] = user_input
    elif booking["phone"] is None and user_input.isdigit():
        booking["phone"] = user_input
    elif booking["booking_type"] is None:
        booking["booking_type"] = user_input
    elif booking["date"] is None:
        booking["date"] = user_input
    elif booking["time"] is None:
        booking["time"] = user_input

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

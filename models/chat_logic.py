from models.booking_flow import (
    initialize_booking_state,
    get_next_question,
    update_booking_state,
    summarize_booking
)
from utils.tools import booking_persistence_tool, email_tool


BOOKING_KEYWORDS = [
    "book", "appointment", "schedule", "consult",
    "visit doctor", "see doctor", "checkup"
]

def detect_booking_intent(user_message: str) -> bool:
    return any(keyword in user_message.lower() for keyword in BOOKING_KEYWORDS)

def handle_user_message(user_message, session_state):
    initialize_booking_state(session_state)

    booking = session_state.booking

    # Confirmation step
    if get_next_question(booking) is None:
        if user_message.lower() in ["yes", "y"]:
            result = booking_persistence_tool(booking)
            if result["success"]:
                booking_id = result["booking_id"]

                email_result = email_tool(
                    booking["email"],
                    booking_id,
                    booking
                )

                session_state.booking = None

                if email_result["success"]:
                    return f"""✅ **Appointment Confirmed!**

            📌 Booking ID: {booking_id}
            📧 Confirmation email sent successfully."""
                else:
                    return f"""✅ **Appointment Confirmed!**

            📌 Booking ID: {booking_id}
            ⚠️ Email could not be sent, but booking was saved."""

        elif user_message.lower() in ["no", "n"]:
            session_state.booking = None
            return "❌ Booking cancelled. Let me know if you want to start again."

        return summarize_booking(booking)

    # Booking flow
    if detect_booking_intent(user_message) or any(value is not None for value in booking.values()):
        error = update_booking_state(booking, user_message)
        if error:
            return error

        next_q = get_next_question(booking)
        return next_q if next_q else summarize_booking(booking)

    return (
        "I can answer clinic-related questions or help you book an appointment 🩺.\n"
        "Just say *book an appointment* to begin."
    )

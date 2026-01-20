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

    user_message_lower = user_message.lower()

    # --------------------------------------------------
    # Get booking if it exists
    # --------------------------------------------------
    booking = session_state.get("booking")

    # --------------------------------------------------
    # CASE 1: Booking already in progress
    # --------------------------------------------------
    if booking is not None:

        # Confirmation stage
        if get_next_question(booking) is None:

            if user_message_lower in ["yes", "y"]:
                result = booking_persistence_tool(booking)

                if result["success"]:
                    booking_id = result["booking_id"]

                    email_result = email_tool(
                        booking["email"],
                        booking_id,
                        booking
                    )

                    session_state.pop("booking")

                    if email_result["success"]:
                        return f"""✅ **Appointment Confirmed!**

📌 Booking ID: {booking_id}
📧 Confirmation email sent successfully."""
                    else:
                        return f"""✅ **Appointment Confirmed!**

📌 Booking ID: {booking_id}
⚠️ Email could not be sent, but booking was saved."""

                return "❌ Booking failed. Please try again later."

            elif user_message_lower in ["no", "n"]:
                session_state.pop("booking")
                return "❌ Booking cancelled. Let me know if you want to start again."

            return "Please reply with **Yes** or **No** to confirm your booking."

        # Slot filling
        error = update_booking_state(booking, user_message)
        if error:
            return error

        next_question = get_next_question(booking)
        if next_question:
            return next_question

        return summarize_booking(booking)

    # --------------------------------------------------
    # CASE 2: Start new booking
    # --------------------------------------------------
    if detect_booking_intent(user_message):
        initialize_booking_state(session_state)
        return "May I know your full name?"

    # --------------------------------------------------
    # CASE 3: Default response
    # --------------------------------------------------
    return (
        "I can help you book an appointment or answer clinic-related questions.\n\n"
        "You can say **book an appointment** to get started."
    )

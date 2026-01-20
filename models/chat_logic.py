from models.booking_flow import (
    initialize_booking_state,
    get_next_question,
    update_booking_state,
    summarize_booking
)

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
            booking["confirmed"] = True
            return "✅ Thank you! Your appointment will be booked shortly."
        elif user_message.lower() in ["no", "n"]:
            session_state.booking = None
            return "❌ Booking cancelled. Let me know if you want to start again."

        return summarize_booking(booking)

    # Booking flow
    if detect_booking_intent(user_message) or any(value is not None for value in booking.values()):
        update_booking_state(booking, user_message)
        next_q = get_next_question(booking)
        return next_q if next_q else summarize_booking(booking)

    return (
        "I can answer clinic-related questions or help you book an appointment 🩺.\n"
        "Just say *book an appointment* to begin."
    )

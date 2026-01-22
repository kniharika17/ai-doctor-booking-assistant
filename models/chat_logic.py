from models.booking_flow import (
    initialize_booking_state,
    get_next_question,
    update_booking_state,
    summarize_booking
)
from utils.tools import booking_persistence_tool, email_tool
from models.rag_pipeline import query_rag

BOOKING_KEYWORDS = [
    "book an appointment",
    "schedule appointment",
    "consult doctor",
    "doctor appointment"
]


def detect_booking_intent(user_message: str) -> bool:
    return any(keyword in user_message.lower() for keyword in BOOKING_KEYWORDS)


def handle_user_message(user_message, session_state):

    booking = session_state.get("booking")

    # ---------------- Booking in progress ----------------
    if booking is not None:

        if get_next_question(booking) is None:
            if user_message.lower() in ["yes", "y"]:
                result = booking_persistence_tool(booking)

                if result["success"]:
                    booking_id = result["booking_id"]
                    email_tool(booking["email"], booking_id, booking)
                    session_state.pop("booking")
                    return f"✅ Appointment confirmed!\nBooking ID: {booking_id}"

                return "❌ Booking failed."

            if user_message.lower() in ["no", "n"]:
                session_state.pop("booking")
                return "❌ Booking cancelled."

            return "Please reply Yes or No."

        error = update_booking_state(booking, user_message)
        if error:
            return error

        next_q = get_next_question(booking)
        return next_q if next_q else summarize_booking(booking)

    # ---------------- Start booking ----------------
    if detect_booking_intent(user_message):
        initialize_booking_state(session_state)
        return "May I know your full name?"

    # ---------------- RAG Answer ----------------
    vectorstore = session_state.get("vectorstore")
    if vectorstore:
        return query_rag(vectorstore, user_message)

    # ---------------- Fallback ----------------
    return "I can help you book an appointment or answer questions from documents."

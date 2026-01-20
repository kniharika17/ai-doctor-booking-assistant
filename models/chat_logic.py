import re

BOOKING_KEYWORDS = [
    "book", "appointment", "schedule", "consult",
    "visit doctor", "see doctor", "checkup"
]

def detect_booking_intent(user_message: str) -> bool:
    message = user_message.lower()
    return any(keyword in message for keyword in BOOKING_KEYWORDS)

def handle_user_message(user_message, chat_history):
    # Limit memory to last 25 messages
    chat_history = chat_history[-25:]

    if detect_booking_intent(user_message):
        return (
            "I can help you book a doctor appointment 🩺.\n\n"
            "To get started, may I know your **full name**?"
        )

    return (
        "I can answer questions about the clinic or help you book an appointment.\n\n"
        "You may upload clinic PDFs and ask questions, or say *book an appointment*."
    )

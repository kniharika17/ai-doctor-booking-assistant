from utils.database import save_booking
from utils.email_service import send_confirmation_email


def booking_persistence_tool(booking_data):
    try:
        booking_id = save_booking(booking_data)
        return {
            "success": True,
            "booking_id": booking_id
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def email_tool(to_email, booking_id, booking):
    try:
        success = send_confirmation_email(
            to_email=to_email,
            booking_id=booking_id,
            booking=booking
        )
        return {
            "success": success
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

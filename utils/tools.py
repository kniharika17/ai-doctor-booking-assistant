from utils.database import save_booking

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

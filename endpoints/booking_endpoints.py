from config.environment_config import ActiveConfig


class BookingEndpoints:
    @staticmethod
    def auth():
        return f"{ActiveConfig.AUTH_URL}"

    @staticmethod
    def booking():
        return f"{ActiveConfig.BOOKING_URL}"

    @staticmethod
    def booking_by_id(booking_id):
        return f"{ActiveConfig.BOOKING_URL}/{booking_id}"

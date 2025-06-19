from config.environment_config import ActiveConfig


class BookingEndpoints:
    @staticmethod
    def auth():
        return f"{ActiveConfig.BASE_URL}{ActiveConfig.AUTH_URL}"

    @staticmethod
    def booking():
        return f"{ActiveConfig.BASE_URL}{ActiveConfig.BOOKING_URL}"

    @staticmethod
    def booking_by_id(booking_id):
        return f"{ActiveConfig.BASE_URL}{ActiveConfig.BOOKING_URL}/{booking_id}"

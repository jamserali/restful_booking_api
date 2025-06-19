def get_auth_payload():
    from config.environment_config import ActiveConfig
    return {
        "username": ActiveConfig.USERNAME,
        "password": ActiveConfig.PASSWORD
    }


def get_booking_payload():
    return {
        "firstname": "Jem",
        "lastname": "Brown",
        "totalprice": 116,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }


def get_updated_booking_payload():
    payload = get_booking_payload()
    payload.update({
        "firstname": "James",
        "totalprice": 111,
        "additionalneeds": "Lunch"
    })
    return payload

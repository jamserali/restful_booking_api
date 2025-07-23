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


def get_partially_update_booking_payload():
    payload = get_booking_payload()
    payload.update({
        "firstname": "Smith",
        "lastname": "ducked"
    })
    return payload


def get_access_token_payload(client_id, client_secret):
    return {
        "grand_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

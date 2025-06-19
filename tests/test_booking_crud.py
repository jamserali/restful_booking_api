import pytest

from data.headers import Headers
from utils.helpers import validate_response, pretty_print
from data.payloads import get_booking_payload, get_updated_booking_payload
from endpoints.booking_endpoints import BookingEndpoints


class TestBookingCRUD:
    def test_create_booking(self, api_client, auth_token):
        """Test creating a new booking"""
        payload = get_booking_payload()
        response = api_client.post(
            BookingEndpoints.booking(),
            headers=Headers.get_json_headers(),
            json=payload
        )
        result = validate_response(response)
        pretty_print(result)
        assert "bookingid" in result
        assert result["booking"] == payload

    def test_get_booking(self, api_client, booking_id):
        """Test retrieving a booking"""
        response = api_client.get(
            BookingEndpoints.booking_by_id(booking_id)
        )
        result = validate_response(response)
        pretty_print(result)

    def test_update_booking(self, api_client, auth_token, booking_id):
        """Test updating a booking"""
        payload = get_updated_booking_payload()
        response = api_client.put(
            BookingEndpoints.booking_by_id(booking_id),
            headers=Headers.get_json_headers(token=auth_token),
            json=payload
        )
        result = validate_response(response)
        pretty_print(result)
        assert result == payload

    def test_delete_booking(self, api_client, auth_token, booking_id):
        """Test deleting a booking"""
        response = api_client.delete(
            BookingEndpoints.booking_by_id(booking_id),
            headers=Headers.get_json_headers(token=auth_token)
        )
        assert response.status_code == 201  # Delete returns 201

        # Verify booking is deleted
        response = api_client.get(
            BookingEndpoints.booking_by_id(booking_id)
        )
        assert response.status_code == 404

import pytest

from data.headers import Headers
from utils.api_client import APIClient
from utils.helpers import validate_response, pretty_print
from data.payloads import get_booking_payload, get_updated_booking_payload, get_partially_update_booking_payload
from endpoints.booking_endpoints import BookingEndpoints


class TestBookingCRUD:
    booking_id = None

    def test_create_booking(self, api_client, auth_token):
        """Test creating a new booking"""
        payload = get_booking_payload()
        response = api_client.post(
            BookingEndpoints.booking(),
            headers=Headers.get_json_headers(),
            json=payload
        )
        TestBookingCRUD.booking_id = response.json()["bookingid"]
        result = validate_response(response)
        pretty_print(result)
        assert "bookingid" in result
        assert result["booking"] == payload

    def test_get_booking(self, api_client):
        """Test retrieving a booking"""
        response = api_client.get(
            BookingEndpoints.booking_by_id(TestBookingCRUD.booking_id)
        )
        result = validate_response(response)
        pretty_print(result)

    def test_update_booking(self, api_client, auth_token):
        """Test updating a booking"""
        payload = get_updated_booking_payload()
        response = api_client.put(
            BookingEndpoints.booking_by_id(TestBookingCRUD.booking_id),
            headers=Headers.get_json_headers(token=auth_token),
            json=payload
        )
        # response = api_client.make_authenticated_request(BookingEndpoints.booking_by_id(booking_id),
        #                                                  headers=Headers.get_json_headers(token=auth_token),
        #                                                  json=payload)

        result = validate_response(response)
        pretty_print(result)
        assert result == payload

        # PartialUpdateBooking
    def test_partial_update_booking(self, api_client, auth_token):

        payload = get_partially_update_booking_payload()
        response = api_client.patch(
                BookingEndpoints.booking_by_id(TestBookingCRUD.booking_id),
                headers=Headers.get_json_headers(token=auth_token),
                json=payload
            )
        assert response.status_code == 200

    def test_delete_booking(self, api_client, auth_token):
        """Test deleting a booking"""
        response = api_client.delete(
            BookingEndpoints.booking_by_id(TestBookingCRUD.booking_id),
            headers=Headers.get_json_headers(token=auth_token)
        )
        assert response.status_code == 201  # Delete returns 201

        # Verify booking is deleted
        response = api_client.get(
            BookingEndpoints.booking_by_id(TestBookingCRUD.booking_id)
        )
        assert response.status_code == 404

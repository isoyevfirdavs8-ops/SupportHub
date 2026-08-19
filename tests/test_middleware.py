import pytest
from django.test import Client


@pytest.mark.django_db
def test_response_time_header():
    client = Client()

    response = client.get(
        "/api/tickets/"
    )

    assert "X-Response-Time" in response
    assert response["X-Response-Time"].endswith("ms")
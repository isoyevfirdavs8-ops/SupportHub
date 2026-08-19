import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from control.models import Ticket


@pytest.mark.django_db
def test_ticket_statistics_is_cached(
    client_user,
    category,
):
    Ticket.objects.create(
        title="Urgent",
        description="Test",
        client=client_user,
        category=category,
        priority="urgent",
        status="new",
    )

    client = APIClient()
    client.force_authenticate(user=client_user)

    cache.clear()

    response1 = client.get(
        "/api/tickets/statistics/"
    )

    assert response1.status_code == 200

    cached = cache.get("ticket_statistics")

    assert cached is not None

    response2 = client.get(
        "/api/tickets/statistics/"
    )

    assert response2.status_code == 200
    assert response1.data == response2.data
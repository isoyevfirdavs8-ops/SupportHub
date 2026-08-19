import pytest
from rest_framework.test import APIClient

from control.models import Ticket


@pytest.mark.django_db
def test_ticket_search(
    client_user,
    category,
):
    Ticket.objects.create(
        title="Internet problem",
        description="WiFi ishlamayapti",
        client=client_user,
        category=category,
    )

    Ticket.objects.create(
        title="Printer",
        description="Printer buzilgan",
        client=client_user,
        category=category,
    )

    client = APIClient()
    client.force_authenticate(user=client_user)

    response = client.get(
        "/api/tickets/?search=internet"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_status_and_priority_filters(
    client_user,
    category,
):
    Ticket.objects.create(
        title="New ticket",
        description="Test",
        client=client_user,
        category=category,
        status="new",
        priority="urgent",
    )

    Ticket.objects.create(
        title="Resolved ticket",
        description="Test",
        client=client_user,
        category=category,
        status="resolved",
        priority="low",
    )

    client = APIClient()
    client.force_authenticate(user=client_user)

    response = client.get(
        "/api/tickets/?status=new&priority=urgent"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
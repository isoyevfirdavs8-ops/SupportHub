import pytest
from rest_framework.test import APIClient

from control.models import Ticket


@pytest.mark.django_db
def test_client_can_create_ticket(
    client_user,
    category,
):
    client = APIClient()
    client.force_authenticate(user=client_user)

    response = client.post(
        "/api/tickets/",
        {
            "title": "Internet",
            "description": "Internet ishlamayapti",
            "category": category.id,
            "priority": "urgent",
        },
        format="json",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_ticket_creator_is_automatically_detected(
    client_user,
    category,
):
    client = APIClient()
    client.force_authenticate(user=client_user)

    response = client.post(
        "/api/tickets/",
        {
            "title": "Printer",
            "description": "Printer ishlamayapti",
            "category": category.id,
        },
        format="json",
    )

    assert response.status_code == 201

    ticket = Ticket.objects.get(
        title="Printer"
    )

    assert ticket.client_id == client_user.id


@pytest.mark.django_db
def test_client_cannot_see_other_clients_ticket(
    client_user,
    second_client,
    ticket,
):
    client = APIClient()
    client.force_authenticate(user=second_client)

    response = client.get(
        f"/api/tickets/{ticket.id}/"
    )

    assert response.status_code in [403, 404]


@pytest.mark.django_db
def test_operator_sees_only_assigned_tickets(
    operator,
    client_user,
    category,
):
    assigned = Ticket.objects.create(
        title="Assigned",
        description="Assigned ticket",
        client=client_user,
        operator=operator,
        category=category,
    )

    Ticket.objects.create(
        title="Not assigned",
        description="Other ticket",
        client=client_user,
        category=category,
    )

    client = APIClient()
    client.force_authenticate(user=operator)

    response = client.get("/api/tickets/")

    assert response.status_code == 200

    ids = [
        item["id"]
        for item in response.data["results"]
    ]

    assert assigned.id in ids
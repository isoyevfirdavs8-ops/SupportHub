import pytest
from rest_framework.test import APIClient

from control.models import Ticket


@pytest.mark.django_db
def test_ticket_pagination(
    client_user,
    category,
):
    Ticket.objects.bulk_create([
        Ticket(
            title=f"Ticket {i}",
            description="Test",
            client=client_user,
            category=category,
        )
        for i in range(25)
    ])

    client = APIClient()
    client.force_authenticate(user=client_user)

    response = client.get(
        "/api/tickets/?page=2&page_size=10"
    )

    assert response.status_code == 200
    assert response.data["count"] == 25
    assert response.data["current_page"] == 2
    assert response.data["page_size"] == 10
    assert len(response.data["results"]) == 10
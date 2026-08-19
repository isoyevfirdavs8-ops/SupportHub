import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_admin_can_create_category(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)

    response = client.post(
        "/api/categories/",
        {
            "name": "Hardware",
        },
        format="json",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_client_cannot_create_category(client_user):
    client = APIClient()
    client.force_authenticate(user=client_user)

    response = client.post(
        "/api/categories/",
        {
            "name": "Hardware",
        },
        format="json",
    )

    assert response.status_code == 403
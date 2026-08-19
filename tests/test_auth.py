import pytest
from rest_framework.test import APIClient

from control.models import User


@pytest.mark.django_db
def test_user_registration():
    client = APIClient()

    response = client.post(
        "auth/register/",
        {
            "username": "newuser",
            "email": "new@test.com",
            "password": "Test12345",
            "password2": "Test12345",
        },
        format="json",
    )

    assert response.status_code in [200, 201]
    assert User.objects.filter(
        username="newuser"
    ).exists()


@pytest.mark.django_db
def test_login_with_wrong_password():
    User.objects.create_user(
        username="ali",
        password="Correct123",
    )

    client = APIClient()

    response = client.post(
        "/api/login/",
        {
            "username": "ali",
            "password": "WrongPassword",
        },
        format="json",
    )

    assert response.status_code in [400, 401]


@pytest.mark.django_db
def test_profile_requires_jwt():
    client = APIClient()

    response = client.get(
        "auth/profile/"
    )

    assert response.status_code == 401
import pytest
from rest_framework.test import APIClient

from control.models import User
from control.models import Category, Ticket


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def client_user(db):
    return User.objects.create_user(
        username="client",
        email="client@test.com",
        password="Test12345",
        role="client",
    )


@pytest.fixture
def second_client(db):
    return User.objects.create_user(
        username="client2",
        email="client2@test.com",
        password="Test12345",
        role="client",
    )


@pytest.fixture
def operator(db):
    return User.objects.create_user(
        username="operator",
        email="operator@test.com",
        password="Test12345",
        role="operator",
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        username="admin",
        email="admin@test.com",
        password="Test12345",
        role="admin",
        is_staff=True,
    )


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Internet",
    )


@pytest.fixture
def ticket(client_user, category):
    return Ticket.objects.create(
        title="Internet problem",
        description="Internet ishlamayapti",
        client=client_user,
        category=category,
        priority=Ticket.PriorityChoices.MEDIUM,
        status=Ticket.StatusChoices.NEW,
    )
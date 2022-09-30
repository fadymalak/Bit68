import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.mark.django_db
@pytest.fixture
def API():
    user = User.objects.create_user(
        username="fadymalak", password="fady123", email="fady@gmail.com"
    )
    Client = APIClient(enforce_csrf_checks=False)
    Client.force_authenticate(user=user)
    return Client


@pytest.mark.django_db
@pytest.fixture
def API_ADMIN():
    user = User.objects.create_superuser(
        username="fadymalak2",
        password="fady123",
        email="fady2@gmail.com",
        is_staff=True,
        is_superuser=True,
    )
    Client = APIClient(enforce_csrf_checks=False)
    Client.force_authenticate(user=user)
    return Client

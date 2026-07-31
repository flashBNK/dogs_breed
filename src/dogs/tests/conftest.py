import pytest
from rest_framework.test import APIClient

from dogs.factories import BreedFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def breed(db):
    return BreedFactory()

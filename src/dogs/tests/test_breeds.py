import pytest
from django.urls import reverse

from dogs.factories import BreedFactory, DogFactory
from dogs.models import Breed


@pytest.mark.django_db
def test_breeds_delete(api_client):
    breed = BreedFactory()
    DogFactory(breed=breed)

    response = api_client.delete(reverse("breeds-detail", args=[breed.id]))

    assert response.status_code == 409
    assert "detail" in response.json()


@pytest.mark.django_db
def test_breed_list(api_client):
    breed_1 = BreedFactory(name="Bulldog")
    breed_2 = BreedFactory(name="Beagle")
    for breed in [breed_1, breed_2]:
        DogFactory(breed=breed, name="Rex")
        DogFactory(breed=breed, name="Balu")

    response = api_client.get(reverse("breeds-list"))

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    for breed in data["results"]:
        assert breed["dogs_count"] == 2


@pytest.mark.django_db
def test_breed_detail(api_client):
    for name in ["Bulldog", "Poodle", "Corgi"]:
        breed = BreedFactory(name=name)

        response = api_client.get(reverse("breeds-detail", args=[breed.id]))

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == name


@pytest.mark.django_db
def test_breed_create(api_client):
    data = {
        "name": "Bulldog",
        "size": Breed.Size.LARGE,
        "friendliness": 2,
        "shedding_amount": 4,
        "exercise_needs": 5,
        "trainability": 3,
    }

    response = api_client.post(reverse("breeds-list"), data=data, format="json")

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Bulldog"


@pytest.mark.django_db
def test_breed_update(api_client):
    breed = BreedFactory(name="Bulldog")

    data = {
        "name": "Corgi",
        "size": Breed.Size.SMALL,
        "friendliness": 2,
        "shedding_amount": 4,
        "exercise_needs": 5,
        "trainability": 3,
    }

    response = api_client.put(reverse("breeds-detail", args=[breed.id]), data=data, format="json")

    assert response.status_code == 200
    breed_updated = response.json()
    assert breed_updated["name"] == "Corgi"

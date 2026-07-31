import pytest
from django.urls import reverse

from dogs.factories import DogFactory


@pytest.mark.django_db
def test_dog_list(api_client, breed):
    DogFactory(breed=breed, age=2, name="Rex")
    DogFactory(breed=breed, age=4, name="Balu")

    response = api_client.get(reverse("dogs-list"))

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    for dog in data["results"]:
        assert dog["average_age"] == 3.0


@pytest.mark.django_db
def test_dog_create(api_client, breed):
    data = {
        "name": "Borya",
        "age": 3,
        "breed": breed.id,
        "gender": "male",
        "color": "black",
        "favorite_food": "meat",
        "favorite_toy": "ball",
    }

    response = api_client.post(reverse("dogs-list"), data=data, format="json")

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Borya"
    assert data["breed"]["id"] == breed.id
    assert data["breed"]["name"] == breed.name


@pytest.mark.django_db
def test_dog_detail(api_client, breed):
    for i, name in {1: "Rex", 2: "Balu", 3: "Borya"}.items():
        dog = DogFactory(breed=breed, age=i, name=name)

        response = api_client.get(reverse("dogs-detail", args=[dog.id]))

        assert response.status_code == 200
        data = response.json()
        assert data["dogs_count"] == i


@pytest.mark.django_db
def test_dog_update(api_client, breed):
    dog = DogFactory(breed=breed, age=4, name="Rex")

    data = {
        "name": "Borya",
        "age": 3,
        "breed": breed.id,
        "gender": "male",
        "color": "black",
        "favorite_food": "meat",
        "favorite_toy": "ball",
    }

    response = api_client.put(reverse("dogs-detail", args=[dog.id]), data=data, format="json")

    assert response.status_code == 200
    dog = response.json()
    assert dog["name"] == "Borya"
    assert dog["age"] == 3


@pytest.mark.django_db
def test_dog_delete(api_client, breed):
    dog = DogFactory(breed=breed, age=4, name="Borya")

    response = api_client.delete(reverse("dogs-detail", args=[dog.id]))

    assert response.status_code == 204

import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from .models import Breed, Dog

DOG_BREED_NAMES = [
    "Labrador Retriever",
    "German Shepherd",
    "Golden Retriever",
    "Bulldog",
    "Poodle",
    "Beagle",
    "Corgi",
]


class BreedFactory(DjangoModelFactory):
    name = FuzzyChoice(DOG_BREED_NAMES)
    size = FuzzyChoice([choice[0] for choice in Breed.Size.choices])
    friendliness = FuzzyInteger(1, 5)
    shedding_amount = FuzzyInteger(1, 5)
    exercise_needs = FuzzyInteger(1, 5)
    trainability = FuzzyInteger(1, 5)

    class Meta:
        model = Breed
        django_get_or_create = ("name",)


class DogFactory(DjangoModelFactory):
    name = factory.Faker("first_name")
    age = FuzzyInteger(1, 30)
    breed = factory.SubFactory(BreedFactory)  # автоматически создаёт породы
    gender = FuzzyChoice([choice[0] for choice in Dog.Gender.choices])
    color = factory.Faker("color")
    favorite_food = factory.Faker("word")
    favorite_toy = factory.Faker("word")

    class Meta:
        model = Dog
        django_get_or_create = ("name", "breed")

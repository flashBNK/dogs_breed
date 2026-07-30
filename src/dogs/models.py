from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Breed(models.Model):
    class Size(models.TextChoices):
        TINY = "tiny", "Tiny"
        SMALL = "small", "Small"
        MEDIUM = "medium", "Medium"
        LARGE = "large", "Large"

    name = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=10, choices=Size)
    friendliness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    shedding_amount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    exercise_needs = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    trainability = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(friendliness__range=(1, 5))
                    & Q(shedding_amount__range=(1, 5))
                    & Q(exercise_needs__range=(1, 5))
                    & Q(trainability__range=(1, 5))
                ),
                name="breed_rating_range",
            ),
        ]

    def __str__(self):
        return self.name


class Dog(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(35)])
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT, related_name="dogs")
    gender = models.CharField(max_length=10, choices=Gender)
    color = models.CharField(max_length=100)
    favorite_food = models.CharField(max_length=100)
    favorite_toy = models.CharField(max_length=100)

    def __str__(self):
        return self.name

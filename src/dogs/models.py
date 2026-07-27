from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q


class Dog(models.Model):
    GENDER_CHOICES = (("male", "Male"), ("female", "Female"))

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    color = models.CharField(max_length=100)
    favorite_food = models.CharField(max_length=100)
    favorite_toy = models.CharField(max_length=100)


class Breed(models.Model):
    class Size(models.TextChoices):
        TINY = "tiny" "Tiny"
        SMALL = "small", "Small"
        MEDIUM = "medium", "Medium"
        LARGE = "large", "Large"

    name = models.CharField(max_length=100)
    size = models.CharField(max_length=100, choices=Size)
    friendliness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    shedding_amount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    exercise_needs = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                        Q(friendliness__range=(1, 5))
                        & Q(shedding_amount__range=(1, 5))
                        & Q(exercise_needs__range=(1, 5))
                ),
                name="breed_rating_range",
            ),
        ]
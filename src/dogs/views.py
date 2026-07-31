from django.db.models import Avg, Count, F, OuterRef, Subquery, Window
from rest_framework.viewsets import ModelViewSet

from .models import Breed, Dog
from .serializers import (
    BreedListSerializer,
    BreedSerializer,
    DogDetailSerializer,
    DogListSerializer,
    DogSerializer,
    DogWriteSerializer,
)
from .speed_tester import speed_queryset


class DogViewSet(ModelViewSet):
    def get_queryset(self):
        if self.action == "list":
            # queryset = Dog.objects.select_related("breed").annotate(average_age=Avg("breed__dogs__age"))
            # плодит квадрат промежуточных строк

            queryset = Dog.objects.select_related("breed").annotate(
                average_age=Window(expression=Avg("age"), partition_by=[F("breed_id")])
            )

            speed_queryset(queryset)
            return queryset

        elif self.action == "retrieve":
            breed_count = (
                Dog.objects.filter(breed=OuterRef("breed")).values("breed").annotate(count=Count("*")).values("count")
            )
            queryset = Dog.objects.select_related("breed").annotate(dogs_count=Subquery(breed_count))

            speed_queryset(queryset)
            return queryset

        return Dog.objects.select_related("breed").all()

    def get_serializer_class(self):
        if self.action == "list":
            return DogListSerializer
        elif self.action == "retrieve":
            return DogDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return DogWriteSerializer

        return DogSerializer


class BreedViewSet(ModelViewSet):
    def get_queryset(self):
        if self.action == "list":
            # queryset = Breed.objects.annotate(dogs_count=Window(expression=Count("dogs"), partition_by=[F("id")]))
            queryset = Breed.objects.annotate(dogs_count=Count("dogs")).order_by("id")  # быстрее, чем через window

            speed_queryset(queryset)
            return queryset

        return Breed.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BreedListSerializer
        return BreedSerializer

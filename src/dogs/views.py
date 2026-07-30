from django.db.models import Avg, Count, F, OuterRef, Subquery, Window
from rest_framework.viewsets import ModelViewSet

from .models import Dog
from .serializers import DogDetailSerializer, DogListSerializer, DogSerializer, DogWriteSerializer
from .speed_tester import speed_queryset


class DogViewSet(ModelViewSet):
    def get_queryset(self):
        if self.action == "list":
            # queryset = Dog.objects.select_related("breed").annotate(average_age=Avg("breed__dogs__age"))

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

        return Dog.objects.select_related().all()

    def get_serializer_class(self):
        if self.action == "list":
            return DogListSerializer
        elif self.action == "retrieve":
            return DogDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return DogWriteSerializer

        return DogSerializer


class BreedViewSet(ModelViewSet):
    pass

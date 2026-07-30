from .models import Dog
from .serializers import DogSerializer, DogListSerializer, DogDetailSerializer
from rest_framework.viewsets import ModelViewSet
from django.db.models.aggregates import Avg
from django.db.models import Count, OuterRef, Subquery
from .speed_tester import speed_queryset


class DogViewSet(ModelViewSet):
    def get_queryset(self):
        if self.action == "list":
            queryset = Dog.objects.select_related("breed").annotate(average_age=Avg("breed__dogs__age"))
            speed_queryset(queryset)
            return queryset

        elif self.action == "retrieve":
            breed_count = Dog.objects.filter(breed=OuterRef("breed")).values("breed").annotate(count=Count("*")).values("count")
            queryset = Dog.objects.select_related("breed").annotate(dogs_count=Subquery(breed_count))
            # print(
            #     queryset.explain(
            #         analyze=True,
            #         verbose=True,
            #         buffers=True,
            #     )
            # )

            return queryset

        return Dog.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return DogListSerializer
        elif self.action == "retrieve":
            return DogDetailSerializer

        return DogSerializer


class BreedViewSet(ModelViewSet):
    pass
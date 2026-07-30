from rest_framework import serializers
from .models import Dog, Breed


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = "__all__"


class DogSerializer(serializers.ModelSerializer):
    breed = BreedSerializer()

    class Meta:
        model = Dog
        fields = "__all__"


class DogListSerializer(serializers.ModelSerializer):
    breed = BreedSerializer()
    average_age = serializers.FloatField(read_only=True)


    class Meta:
        model = Dog
        fields = ["id", "name", "age", "breed", "gender", "color", "favorite_food", "favorite_toy", "average_age"]



class DogDetailSerializer(serializers.ModelSerializer):
    breed = BreedSerializer()
    dogs_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = ["name", "age", "breed", "gender", "color", "favorite_food", "favorite_toy", "dogs_count"]

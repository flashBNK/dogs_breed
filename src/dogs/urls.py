from rest_framework.routers import DefaultRouter

from .views import BreedViewSet, DogViewSet

router = DefaultRouter()
router.register(r"dogs", DogViewSet, basename="dogs")
router.register(r"breeds", BreedViewSet, basename="breeds")

urlpatterns = router.urls

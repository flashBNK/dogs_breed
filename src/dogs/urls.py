from rest_framework.routers import DefaultRouter

from .views import DogViewSet

router = DefaultRouter()
router.register(r"dogs", DogViewSet, basename="dogs")

urlpatterns = router.urls

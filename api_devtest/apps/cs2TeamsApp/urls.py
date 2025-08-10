from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, TypePlayerViewSet

router = DefaultRouter()

router.register(r"players", PlayerViewSet, basename="players")
router.register(r"type_players", TypePlayerViewSet, basename="type_players")

urlpatterns = [
    path("", include(router.urls)),
]
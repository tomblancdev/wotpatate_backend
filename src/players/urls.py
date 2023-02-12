from django.urls import path
from rest_framework import routers

from .views import PlayerTokenViewSet, PlayerViewSet

router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'token', PlayerTokenViewSet)

urlpatterns = router.urls

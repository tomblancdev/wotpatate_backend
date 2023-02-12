from rest_framework import routers

from .views import PlayerViewSet, PlayerTokenViewSet

router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'token', PlayerTokenViewSet)

urlpatterns = router.urls

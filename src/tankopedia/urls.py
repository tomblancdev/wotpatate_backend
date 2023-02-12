from django.urls import path

from rest_framework import routers

from .views import TankViewSet, update_tankopedia

router = routers.DefaultRouter()
router.register(r'tanks', TankViewSet)


urlpatterns = [
    path('update/', update_tankopedia),
] + router.urls

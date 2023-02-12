from django.urls import path
from rest_framework import routers

from .views import PlayerViewSet, register, add_token

router = routers.DefaultRouter()
router.register(r'', PlayerViewSet)

urlpatterns = router.urls + [
    path('register/', register),
    path('add_token/', add_token),
]

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Player, PlayerToken
from .serializers import PlayerSerializer, PlayerTokenSerializer


class PlayerViewSet(ReadOnlyModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    search_fields = ('nickname')

    def list(self, request, *args, **kwargs):
        if self.queryset.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        if self.queryset.count() > 5:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'error': 'Too many players'})
        return super().list(request, *args, **kwargs)


class PlayerTokenViewSet(ModelViewSet):
    queryset = PlayerToken.objects.all()
    serializer_class = PlayerTokenSerializer

    def create(self, request, *args, **kwargs):
        if self.queryset.count() == 0:
            return super().create(request, *args, **kwargs)
        # update token if exists
        instance = self.queryset.first()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

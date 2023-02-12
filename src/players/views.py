
import requests

from rest_framework import filters

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from .models import Player, PlayerToken, User
from .serializers import PlayerSerializer, PlayerTokenSerializer, UserSerializer

from utils.WOT_API import refresh_player_access_token


class PlayerViewSet(ReadOnlyModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('nickname',)
    lookup_field = 'nickname'

    def list(self, request, *args, **kwargs):
        if self.queryset.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        if self.queryset.count() > 5:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'error': 'Too many players'})
        return super().list(request, *args, **kwargs)


@api_view(['POST'])
def register(request):
    user_id = request.user.id
    data = {**request.data, 'user_id': user_id}
    serializer = PlayerSerializer(data=data)
    if serializer.is_valid():
        player = serializer.save()
        if player:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_token(request):
    player_id = request.user.player.account_id
    token = request.data.get('token')
    expires_at = request.data.get('expires_at')
    # check if token is valid from wot api
    new_token = refresh_player_access_token(token)
    print(new_token)
    if new_token["status"] == "error":
        return Response(data={'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    # save new token
    token = new_token["data"]["access_token"]
    expires_at = new_token["data"]["expires_at"]
    # check if player is owner of token
    if new_token["data"]["account_id"] != player_id:
        return Response(status=status.HTTP_403_FORBIDDEN, data={'error': 'Invalid token'})
    data = {
        'token': token,
        'expires_at': expires_at,
        'player_id': player_id
    }
    serializer = PlayerTokenSerializer(data=data)
    if serializer.is_valid():
        player_token = serializer.save()
        if player_token:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

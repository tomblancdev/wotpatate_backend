from rest_framework import serializers

from website.serializers import UserSerializer

from .models import Player, PlayerToken, User


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Player
        fields = ('account_id', 'nickname', 'user')


class PlayerTokenSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = PlayerToken
        fields = ('token', 'expires_at', 'player')

    def create(self, validated_data):
        player_data = validated_data.pop('player')
        user_data = player_data.pop('user')
        user = User.objects.create_user(**user_data)
        player = Player.objects.create(user=user, **player_data)
        token = PlayerToken.objects.create(player=player, **validated_data)
        return token

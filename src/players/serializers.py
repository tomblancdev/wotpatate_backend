from rest_framework import serializers

from website.serializers import UserSerializer

from .models import Player, PlayerToken, User


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Player
        fields = ('account_id', 'user', 'nickname', 'user_id')
        extra_kwargs = {
            'account_id': {'write_only': True},
        }

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.get(pk=user_id)
        player = Player.objects.create(user=user, **validated_data)
        return player


class PlayerTokenSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    player_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PlayerToken
        fields = ('token', 'expires_at', 'player', 'player_id')

    def create(self, validated_data):
        player_id = validated_data.pop('player_id')
        player = Player.objects.get(pk=player_id)
        # create or update player token
        player_token, created = PlayerToken.objects.update_or_create(
            player=player, defaults=validated_data)
        return player_token

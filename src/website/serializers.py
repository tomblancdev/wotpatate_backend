from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True},
                        'password2': {'write_only': True}}

    def create(self, validated_data):
        # check if passwords match
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match'})
            # check password contains at least 8 characters and at least one number and one letter and one special character and no spaces and one uppercase and one lowercase
        if len(password) < 8:
            raise serializers.ValidationError(
                {'password': 'Password must be at least 8 characters'})
        elif not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                {'password': 'Password must contain at least one number'})
        elif not any(char.isalpha() for char in password):
            raise serializers.ValidationError(
                {'password': 'Password must contain at least one letter'})
        elif not any(not char.isalnum() for char in password):
            raise serializers.ValidationError(
                {'password': 'Password must contain at least one special character'})
        elif any(char.isspace() for char in password):
            raise serializers.ValidationError(
                {'password': 'Password must not contain spaces'})
        elif not any(char.isupper() for char in password):
            raise serializers.ValidationError(
                {'password': 'Password must contain at least one uppercase letter'})
        elif not any(char.islower() for char in password):
            raise serializers.ValidationError(
                {'password': 'Password must contain at least one lowercase letter'})
        user = User.objects.create_user(**validated_data, password=password)
        return user

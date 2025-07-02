from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True)
    
    # For output
    profile_role = serializers.SerializerMethodField()

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        Profile.objects.create(user=user, role=role)
        return user

    def get_profile_role(self, obj):
        return obj.profile.role


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

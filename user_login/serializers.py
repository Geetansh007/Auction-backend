from rest_framework import serializers
from .models import User, Celebrity

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile_number', 'password', 'profile_image', 'date_joined', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            mobile_number=validated_data['mobile_number'],
            password=validated_data['password']
        )
        return user

class CelebritySignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Celebrity
        fields = ['id', 'username', 'mobile_number', 'password', 'profile_image', 'bio', 'date_joined', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        celebrity = Celebrity.objects.create(
            username=validated_data['username'],
            mobile_number=validated_data['mobile_number'],
            password=validated_data['password']
        )
        return celebrity
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class CelebrityLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
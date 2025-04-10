from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from store.serializers.user_serializers import UserSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Sử dụng UserSerializer để lấy thông tin người dùng
        user_serializer = UserSerializer(user)
        data['user'] = user_serializer.data

        return data
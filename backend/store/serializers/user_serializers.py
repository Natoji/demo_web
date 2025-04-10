from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname', 'password'] 
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            fullname=validated_data.get('fullname'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user

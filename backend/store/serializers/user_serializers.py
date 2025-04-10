# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'fullname', 'password'] 
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User(
#             email=validated_data.get('email'),
#             fullname=validated_data.get('fullname'),
#         )
#         user.set_password(validated_data.get('password'))
#         user.save()
#         return user
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)  # Thêm trường role, read-only vì đã có default trong model

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname', 'password', 'role'] # Thêm 'role' vào danh sách fields
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            fullname=validated_data.get('fullname'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        # Cho phép cập nhật các trường khác nếu cần
        instance.email = validated_data.get('email', instance.email)
        instance.fullname = validated_data.get('fullname', instance.fullname)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance
# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken
# from store.serializers.user_serializers import UserSerializer

# User = get_user_model()

# # Register
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]

# # Logout (invalidate refresh token)
# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data.get("refresh")
#             if not refresh_token:
#                 return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

#             token = RefreshToken(refresh_token)
#             token.blacklist()  # Phương thức blacklist() sau khi cấu hình
#             return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # Get current user info
# class UserProfileView(generics.RetrieveAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from store.serializers.user_serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

# Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Logout (invalidate refresh token)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Phương thức blacklist() sau khi cấu hình
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Get current user info
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Custom Login View to return user info
class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.user
        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']
        user_serializer = UserSerializer(user)

        return Response({
            'refresh': str(refresh),
            'access': str(access),
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)
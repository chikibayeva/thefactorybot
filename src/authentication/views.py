from django.contrib.auth.models import User
from rest_framework import views
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import serializers


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegistrationSerializer


class LoginApiView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=200)


class LogOutView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "logout success"}, status=200)
        except User.DoesNotExist:
            return Response({"message": "user unauthorized"}, status=401)

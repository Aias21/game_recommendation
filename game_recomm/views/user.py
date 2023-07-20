from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from ..serializers import RegisterUserSerializer, LoginUserSerializer
from django.contrib.auth import login, authenticate, logout
from rest_framework.permissions import AllowAny


class RegisterUser(APIView):
    permission_classes = [AllowAny] #  allow any user to register

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get("username")
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = True
            user.save()
            # create token for user
            Token.objects.create(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LoginUser(APIView):
    # permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get("username")
            password = serializer.data.get("password")
            user = authenticate(username=username, password=password)
            try:
                token = Token.objects.get(user=user)
                data = {"token": str(token), "username": username}
                status = 200
            except:
                data = serializer.errors
                status = 401
            finally:
                return Response(data, status=status)

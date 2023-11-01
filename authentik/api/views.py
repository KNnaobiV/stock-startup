from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password
from django.shortcuts import reverse

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from authentik.api.serializers import *

__all__ = [
    "ChangePasswordView",
    "LoginView",
    "LogoutView",
    "LogoutAllView",
    "RegisterAPI",
    "PortfolioDetailAPI",
    "ProfileAPI",
    "ProfileView",
    "RegisterView",
    "TradeCreateAPI",
    "TradeDetailAPI",
    "UpdateProfileView",
]

User = get_user_model()

class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = PairTokenSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializers):
        password = make_password(serializer.validated_data.get('password'))
        serializer.save(password=password)


class ChangePasswordView(UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class ProfileAPI(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        return Response({'url': reverse('profile_api'),})


class ProfileView(generics.RetrieveAPIView):
    queryset = DefaultUser.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'


class PortfolioDetailAPI(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_claass = PortfolioSerializer
    lookup_field = 'name'


class TradeCreateAPI(generics.CreateAPIView):
    queryset = Trade.objects.all()
    serializer = TradeSerializer
    

class TradeDetailAPI(generics.RetrieveAPIView):
    queryset = Trade.objects.all()
    serializer = TradeSerializer
    lookup_field = 'uuid'


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


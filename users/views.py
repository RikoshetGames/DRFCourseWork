from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Создание пользователя"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    """Список пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDetailAPIView(generics.RetrieveAPIView):
    """Подробная информация о пользователе"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    """Редактирование пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Удаление пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

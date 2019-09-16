from rest_framework import viewsets
from rest_framework import mixins
from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

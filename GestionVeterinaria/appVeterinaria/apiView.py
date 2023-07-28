from rest_framework import generics
from appVeterinaria.models import *
from appVeterinaria.serializers import UserSerializer

class userList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


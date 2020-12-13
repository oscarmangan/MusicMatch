from django.shortcuts import render
from rest_framework import viewsets
from musicapp.serializers import UserSerializer, ProfileSerializer, InstrumentSerializer, GenreSerializer
from django.contrib.auth.models import User
from musicapp.models import Profile, Genre, Instrument


# ViewSets for all model serializers below
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class InstrumentViewSet(viewsets.ModelViewSet):
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from musicapp.serializers import *
from django.contrib.auth.models import User
from musicapp.models import Profile, Instrument, Genre, UserInstrument, UserGenre


# ViewSets for all model serializers below
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    authentication_classes = (TokenAuthentication,)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    authentication_classes = (TokenAuthentication, )


class InstrumentViewSet(viewsets.ModelViewSet):
    serializer_class = InstrumentSerializer
    queryset = Instrument.objects.all()
    authentication_classes = (TokenAuthentication,)


class UserInstrumentViewSet(viewsets.ModelViewSet):
    serializer_class = UserInstrumentSerializer
    queryset = UserInstrument.objects.all()
    authentication_classes = (TokenAuthentication,)


class UserGenreViewSet(viewsets.ModelViewSet):
    serializer_class = UserGenreSerializer
    queryset = UserGenre.objects.all()
    authentication_classes = (TokenAuthentication,)

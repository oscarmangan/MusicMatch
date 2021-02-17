from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from musicapp.serializers import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from musicapp.models import Profile, Instrument, Genre, UserInstrument, UserGenre
from rest_framework.authtoken.models import Token


# ViewSets for all model serializers below
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication, )


class CreateUserViewSet(viewsets.ModelViewSet):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    # POST request to CreateUserViewSet where we create a new account
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    authentication_classes = (TokenAuthentication, )


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


class UserImageViewSet(viewsets.ModelViewSet):
    serializer_class = UserImageSerializer
    queryset = UserImage.objects.all()
    authentication_classes = (TokenAuthentication,)

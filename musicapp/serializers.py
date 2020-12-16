from rest_framework import serializers
from django.contrib.auth.models import User
from musicapp.models import Genre, Instrument, Profile, UserGenre, UserInstrument


# Serializer for User class, returning ID, username, email and superuser status
class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'password')


# Serializer for Profile class, returning users profile details
class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'phone', 'age', 'band_exp', 'location', 'lat_long')


# Serializer for Genre class, returning ID and genre name
class GenreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'genre_name')


# Serializer for Instrument class, returning ID and instrument type
class InstrumentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Instrument
        fields = ('id', 'instrument_name')


class UserGenreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserGenre
        fields = ('user', 'genre')


class UserInstrumentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserInstrument
        fields = ('user', 'instrument', 'experience_level')

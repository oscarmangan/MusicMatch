from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework import serializers
from django.contrib.auth.models import User
from musicapp.models import Genre, Instrument, Profile, UserGenre, UserInstrument, UserImage
from rest_framework.authtoken.models import Token


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ('bio', 'age', 'band_exp',
                  'facebook_url', 'twitter_url', 'instagram_url',
                  'town', 'lat_long')


# Serializer for User class, returning ID, username, email and superuser status
class UserSerializer(serializers.HyperlinkedModelSerializer):

    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile',)
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    # Create a new user
    def create(self, validated_data):

        # Create a new User model with the authentication data
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)

        # Create the profile to coincide with the new User
        print(profile_data)
        profile = Profile.objects.create(
            user=user,
            **profile_data
        )

        # Create the UserGenre rows to coincide with the new User
        # genre_data = validated_data.pop('genres')
        # Create the UserInstrument rows to coincide with the new User
        # instrument_data = validated_data.pop('instruments')
        # Create the UserImage rows to coincide with the new User
        # image_data = validated_data.pop('images')

        return user

        # # Create a row in the link table for each genre attached in the request to the user
        # for gen in validated_data['genres']:
        #     user_genre = UserGenre.objects.create(
        #         user=user,
        #         genre=gen
        #     )
        #
        # # Create a row in the link table for each instrument and experience level
        # for ins in validated_data['instruments']:
        #     user_instrument = UserInstrument.objects.create(
        #         user=user,
        #         instrument=ins.name,
        #         experience_level=ins.exp
        #     )
        #
        # # Create a row in the link table for each image uploaded
        # for img in validated_data['images']:
        #     if img is not None:
        #         user_image = UserImage.objects.create(
        #             user=user,
        #             image=img
        #

    # def create(self, validated_data):
    #
    #     username = validated_data['user']
    #     profile = Profile.objects.create(
    #         user=User.objects.get(username=username),
    #         bio=validated_data['bio'],
    #         age=validated_data['age'],
    #         band_exp=validated_data['band_exp'],
    #         facebook_url=validated_data['facebook'],
    #         twitter_url=validated_data['twitter'],
    #         instagram_url=validated_data['instagram'],
    #         town=validated_data['town'],
    #         lat_long=validated_data['lat_long']
    #     )
    #
    #     return profile


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


# Serializer for UserGenre class, this class holds each genre associated to each user
class UserGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserGenre
        fields = ('user', 'genre')


# Serializer for UserInstrument class, this class holds each instrument played by each user
# also holding the level of exp (in years) for that combination
class UserInstrumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInstrument
        fields = ('user', 'instrument', 'experience_level')


# Serializer for UserImage class, this class holds each users image uploaded
class UserImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserImage
        fields = ('user', 'image')

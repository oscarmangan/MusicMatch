from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework import serializers
from django.contrib.auth.models import User
from musicapp.models import Genre, Instrument, Profile, UserGenre, UserInstrument, UserImage
from rest_framework.authtoken.models import Token


# Serializer for User class, returning ID, username and email
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'age', 'band_exp',
                  'facebook_url', 'twitter_url', 'instagram_url', 'music_url',
                  'town', 'lat_long', 'distance_limit',)


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
class UserGenreSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

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


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):

    profile = ProfileSerializer(required=True)
    genres = UserGenreSerializer(required=True, many=True)
    # instruments = UserInstrumentSerializer(required=True, many=True)
    # images = UserImageSerializer(required=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile', 'genres')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    User = get_user_model()

    # Create a new user
    def create(self, validated_data):
        # Separate the JSON data into individual objects
        print(validated_data)
        profile_data = validated_data.pop('profile')
        genres_data = validated_data.pop('genres')
        # instruments_data = validated_data.pop('instruments')
        # images_data = validated_data.pop('images')

        # Create the User object
        user = User()
        user.email = validated_data['email']
        user.username = validated_data['username']
        user.set_password(raw_password=validated_data['password'])
        user.is_superuser = "0"
        user.is_staff = "0"
        user.save()
        Token.objects.create(user=user)

        # Handling coordinates from the data
        coords = profile_data['lat_long'].split(",")
        new_coords = [float(part) for part in coords]
        point = Point(new_coords, srid=4326)

        # Create the profile to coincide with the new User
        profile = Profile.objects.create(
            user=user,
            band_exp=profile_data['band_exp'],
            age=profile_data['age'],
            lat_long=point,
            bio=profile_data['bio'],
            town=profile_data['town'],
            distance_limit=profile_data['distance_limit'],
            music_url=profile_data['music_url'],
            twitter_url=profile_data['twitter_url'],
            instagram_url=profile_data['instagram_url'],
            facebook_url=profile_data['facebook_url'],
        )

        # Loop through all of the genres passed and create a UserGenre object for each
        for i in genres_data:
            value = i['genre']
            genres = UserGenre.objects.create(
                user=user,
                genre=value
            )

        # for i in instruments_data:
        #     ins_name = instruments_data[i]['instrument']
        #     instrument = Instrument.objects.get(instrument_name=ins_name)
        #     exp = int(instruments_data[i]['exp'])
        #     instruments = UserInstrument.objects.create(
        #         user=user,
        #         instrument=instrument,
        #         experience_level=exp
        #     )

        return user


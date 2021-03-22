from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework import serializers
from django.contrib.auth.models import User
from musicapp.models import Genre, Instrument, Profile, UserGenre, UserInstrument, UserImage, UserRecommendation
from rest_framework.authtoken.models import Token


# Custom RelationField class to get the url of the images without needing the entire UserImageSerializer
class ImageListingField(serializers.RelatedField):

    def to_representation(self, value):
        return value.image_file.url


class InstrumentListingField(serializers.RelatedField):

    def to_representation(self, value):
        data = {"instrument": value.instrument.id, "name": value.instrument.instrument_name, "experience_level": value.experience_level}
        return data


class GenreListingField(serializers.RelatedField):

    def to_representation(self, value):
        data = {"genre": value.genre.id, "name": value.genre.genre_name}
        return data


# Serializer for Profile class
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('user_id', 'bio', 'age', 'band_exp',
                  'facebook_url', 'twitter_url', 'instagram_url', 'music_url',
                  'town', 'lat_long', 'distance_limit',)


# Serializer for User class, returning ID, username and email
class UserSerializer(serializers.HyperlinkedModelSerializer):

    images = ImageListingField(many=True, read_only=True)
    instruments = InstrumentListingField(many=True, read_only=True)
    genres = GenreListingField(many=True, read_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'images', 'profile',
                  'instruments', 'genres')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


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
class UserInstrumentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserInstrument
        fields = ('user', 'instrument', 'experience_level')


# Serializer for UserImage class, this class holds each users image uploaded
class UserImageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserImage
        fields = ('user', 'image_file')


# Serializer for the creation of one or multiple UserImage models for photo uploading
class CreateUserImageSerializer(serializers.ModelSerializer):
    images = UserImageSerializer(required=True, many=True)

    class Meta:
        model = UserImage
        fields = ('user', 'images')

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        user = validated_data['user']
        for i in images_data:
            value = i['image_file']
            UserImage.objects.create(
                user=user,
                image_file=value
            )

        return user


# Serializer for creating a user with multiple other model instances created
class CreateUserSerializer(serializers.HyperlinkedModelSerializer):

    profile = ProfileSerializer(required=True)
    genres = UserGenreSerializer(required=True, many=True)
    instruments = UserInstrumentSerializer(required=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile',
                  'genres', 'instruments')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    User = get_user_model()

    # Create a new user
    def create(self, validated_data):
        # Separate the JSON data into individual objects
        profile_data = validated_data.pop('profile')
        genres_data = validated_data.pop('genres')
        instruments_data = validated_data.pop('instruments')

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
        profile.save()

        # Loop through all of the genres passed and create a UserGenre object for each
        for i in genres_data:
            value = i['genre']
            genres = UserGenre.objects.create(
                user=user,
                genre=value
            )
            genres.save()

        # Loop through all of the instruments passed and create a UserInstrument object for each
        for i in instruments_data:
            instrument = i['instrument']
            exp_lvl = i['experience_level']
            instruments = UserInstrument.objects.create(
                user=user,
                instrument=instrument,
                experience_level=exp_lvl
            )
            instruments.save()

        return user


# Update the users profile serializer
class UpdateUserSerializer(serializers.HyperlinkedModelSerializer):

    profile = ProfileSerializer(required=True)
    genres = UserGenreSerializer(required=True, many=True)
    instruments = UserInstrumentSerializer(required=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile',
                  'genres', 'instruments')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def update(self, instance, validated_data):

        # checking if the profile object is in the request passed to the view
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            profile = instance.profile

            # set the new values for each possible updatable field
            profile.bio = profile_data.get('bio', profile.bio)
            profile.age = profile_data.get('age', profile.age)
            profile.facebook_url = profile_data.get('facebook_url', profile.facebook_url)
            profile.twitter_url = profile_data.get('twitter_url', profile.twitter_url)
            profile.instagram_url = profile_data.get('instagram_url', profile.instagram_url)
            profile.music_url = profile_data.get('music_url', profile.music_url)
            profile.town = profile_data.get('town', profile.town)
            profile.band_exp = profile_data.get('band_exp', profile.band_exp)
            profile.distance_limit = profile_data.get('distance_limit', profile.distance_limit)
            profile.save()

        # checking that instruments array was passed in the request
        if 'instruments' in validated_data:
            instruments_data = validated_data.pop('instruments')

            # delete all previous entries of instruments for this user
            UserInstrument.objects.filter(user=instance).delete()

            # create the one or many new UserInstrument objects
            for i in instruments_data:
                instruments = UserInstrument.objects.create(
                    user=instance,
                    instrument=i['instrument'],
                    experience_level=i['experience_level']
                )
                instruments.save()

        # checking that genres array was passed in the request
        if 'genres' in validated_data:
            genres_data = validated_data.pop('genres')

            # delete all previous entries of genres for this user
            UserGenre.objects.filter(user=instance).delete()

            # Loop through all of the genres passed and create a UserGenre object for each
            for i in genres_data:
                genres = UserGenre.objects.create(
                    user=instance,
                    genre=i['genre']
                )
                genres.save()

        return instance


# Serializer for the UserRecommendation model
class UserRecommendationsSerializer(serializers.ModelSerializer):

    recommendation = UserSerializer()

    class Meta:
        model = UserRecommendation
        fields = ('user', 'recommendation', 'distance_from_user', 'score')


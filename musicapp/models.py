from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Model for profile, 1-to-1 relationship with User model/entity
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=400, blank=True, null=True, default=None)
    age = models.IntegerField(null=True, default=None, validators=[MinValueValidator(13)])
    band_exp = models.IntegerField(null=False, default=None, validators=[MinValueValidator(0)])
    distance_limit = models.IntegerField(null=False, default=50, validators=[MinValueValidator(1), MaxValueValidator(100)])
    town = models.CharField(max_length=40, blank=True, null=True, default=None)
    music_url = models.URLField(max_length=100, null=True, blank=True, default=None)
    facebook_url = models.URLField(max_length=100, null=True, blank=True, default=None)
    twitter_url = models.URLField(max_length=100, null=True, blank=True, default=None)
    instagram_url = models.URLField(max_length=100, null=True, blank=True, default=None)
    lat_long = models.PointField(
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        return f'{self.user}'


# Model for each instrument type (e.g. Piano, Vocals, Drums)
class Instrument(models.Model):
    instrument_name = models.CharField('instrument_type', max_length=50, unique=True)

    def __str__(self):
        return self.instrument_name


# Model for genres (e.g. Rock, Pop, Metal, Classical)
class Genre(models.Model):
    genre_name = models.CharField('genre', max_length=50, unique=True)

    def __str__(self):
        return self.genre_name


# Link tables below. User and instrument/genre act as composite keys

# Model for UserInstruments (link table between User and Instruments)
class UserInstrument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instruments")
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    experience_level = models.IntegerField('instrument_exp', null=False, default=None)

    class Meta:
        unique_together = (('user', 'instrument'),)
        index_together = (('user', 'instrument'),)


# Model for UserGenre (link table between User and genres)
class UserGenre(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="genres")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'genre'),)
        index_together = (('user', 'genre'),)


def upload_path(instance, filename):
    return '/'.join(['user_images', str(instance.user.id), filename])


# Model for UserImages where each users profile stores a maximum of 3 images for profile display
class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(null=True, blank=True, upload_to=upload_path)


# Model for UserRecommendations where we store a row for each user along with the other user IDs they have been recommended
class UserRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thisuser')
    recommendation = models.ForeignKey(User, on_delete=models.CASCADE)
    distance_from_user = models.FloatField('distance_from_user', null=False, default=0)
    score = models.FloatField('rec_score', null=False, default=0)

    class Meta:
        unique_together = (('user', 'recommendation'),)
        index_together = (('user', 'recommendation'),)

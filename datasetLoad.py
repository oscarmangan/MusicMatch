# File to load the dataset into the Django system
import csv
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from musicapp.models import Profile, Instrument, Genre, UserGenre, UserInstrument
from rest_framework.authtoken.models import Token

datasetFile = 'dataset_mm.csv'
data = csv.reader(open(datasetFile), delimiter=',')
next(data)  # skip the first line
User = get_user_model()

# Loop through the file
for row in data:

    # Creating the User object
    new_user = User()
    new_user.email = row[0]
    new_user.username = row[1]
    new_user.set_password(raw_password=row[2])
    new_user.is_superuser = "0"
    new_user.is_staff = "0"
    new_user.save()
    Token.objects.create(user=new_user)

    # Handling coordinates which are longitude,latitude
    # Our application handles it as latitude,longitude
    coords = row[15].split(",")
    latlon = [coords[1], coords[0]]
    newCoords = [float(part) for part in latlon]

    point = Point(newCoords, srid=4326)

    # Creating the Profile object
    new_profile = Profile.objects.create(
        user=new_user,
        band_exp=row[12],
        age=row[13],
        lat_long=point,
        bio=row[17],
        town=row[16]
    )
    new_profile.save()

    # Creating UserGenre 1 object
    ug_1 = UserGenre.objects.create(
        user=new_user,
        genre=Genre.objects.get(genre_name=row[9])
    )
    ug_1.save()

    # Creating UserGenre 2 object
    if row[10] != "":
        ug_2 = UserGenre.objects.create(
            user=new_user,
            genre=Genre.objects.get(genre_name=row[10])
        )
        ug_2.save()

    # Creating UserGenre 3 object
    if row[11] != "":
        ug_3 = UserGenre.objects.create(
            user=new_user,
            genre=Genre.objects.get(genre_name=row[11])
        )
        ug_3.save()

    # Creating UserInstrument 1 object
    ui_1 = UserInstrument.objects.create(
        user=new_user,
        instrument=Instrument.objects.get(instrument_name=row[3]),
        experience_level=row[4]
    )
    ui_1.save()

    # Creating UserInstrument 2 object
    if row[5] != "":
        ui_2 = UserInstrument.objects.create(
            user=new_user,
            instrument=Instrument.objects.get(instrument_name=row[5]),
            experience_level=row[6]
        )
        ui_2.save()

    # Creating UserInstrument 3 object
    if row[7] != "":
        ui_3 = UserInstrument.objects.create(
            user=new_user,
            instrument=Instrument.objects.get(instrument_name=row[7]),
            experience_level=row[8]
        )
        ui_3.save()

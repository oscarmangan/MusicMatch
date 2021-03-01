import pandas as pd
import numpy as np
import geopy.distance
from musicapp.models import Profile, User


# Function to filter out users outside the current users location limit
def checkUsersWithinLimit(username):
    print("in function")

    # Get the users profile, location(Point) and loc_limit(km radius limit)
    user = User.objects.get(username=username)
    print(user)
    curr_profile = Profile.objects.get(user=user)
    user_location = curr_profile.lat_long
    loc_limit = curr_profile.distance_limit
    counter = 0

    # Using GeoPy library, we calculate the distance between (in km) between
    # the current users location and the location of each user in the database
    for i in Profile.objects.all():
        if geopy.distance.distance(user_location, i.lat_long).km <= loc_limit:
            print(i.town, geopy.distance.distance(user_location, i.lat_long))
            counter += 1

    print("Total users within distance limit: " + str(loc_limit) + " is " + str(counter))


checkUsersWithinLimit("rachellai21")

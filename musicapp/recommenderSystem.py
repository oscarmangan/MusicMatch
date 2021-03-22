import pandas as pd
import numpy as np
import geopy.distance
from num2words import num2words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance
from musicapp.models import Profile, User, UserInstrument, UserGenre, UserRecommendation

genres_list = ['alternative', 'blues', 'classical', 'country', 'disco', 'electronic', 'hip-hop', 'indie',
               'jazz', 'metal', 'pop', 'r&b', 'reggae', 'rock', 'traditional']

instruments_list = ['accordian', 'acoustic guitar', 'banjo', 'bass guitar', 'cello', 'clarinet', 'double bass',
                    'drums', 'electric guitar', 'flute', 'harp', 'mandelin', 'piano', 'saxophone', 'trombone',
                    'trumpet', 'tuba', 'viola', 'violin', 'vocalist', 'xylophone']


# Function to filter out users outside the current users location limit
def dataPreProcessing(user_id):

    # Get the users profile, location(Point) and loc_limit(km radius limit)
    user = User.objects.get(id=user_id)
    curr_profile = Profile.objects.get(user=user)
    user_location = curr_profile.lat_long
    loc_limit = curr_profile.distance_limit
    index_counter = -1

    # Create an empty DataFrame with two columns, user ID and distance to current user
    # and convert the user_id column to int
    potential_users = pd.DataFrame(columns=['user_id', 'distance_to_user', 'genres_data',
                                            'instruments_data', 'ins_exp_data', 'band_data', 'similarity_score'])

    # Using GeoPy library, we calculate the distance between (in km) between
    # the current users location and the location of each user in the database
    for index, value in enumerate(Profile.objects.all()):
        distance_between_users = geopy.distance.distance(user_location, value.lat_long).km

        # If the user is within the location threshold, then get this users instruments,
        # instrument experience, band experience and genres and add them to the DataFrame
        if distance_between_users <= loc_limit and distance_between_users <= value.distance_limit:
            index_counter += 1
            user_instruments = UserInstrument.objects.filter(user=value.user)
            user_genres = UserGenre.objects.filter(user=value.user)
            genres_data = np.zeros(15)
            instruments_data = np.zeros(21)
            ins_exp_data = np.zeros(21)

            # For each user, create a list of the genre names and a list of the instruments with experience
            # We must also remove the spaces in the names to make them unique (e.g. electricguitar)
            for i in user_genres:
                index = genres_list.index(i.genre.genre_name.lower())
                genres_data[index] = 1

            # For instruments, we append the experience in years number as a word to the name of the instrument
            # to make it unique, for example cello5 and cello5 are the same instrument and experience level
            for i in user_instruments:
                index = instruments_list.index(i.instrument.instrument_name.lower())
                instruments_data[index] = 1
                ins_exp_data[index] = i.experience_level

            potential_users.loc[index_counter] = [value.user.id, distance_between_users,
                                                  genres_data, instruments_data, ins_exp_data, value.band_exp, ""]

    potential_users['user_id'] = potential_users['user_id'].astype(int)
    return getRecommendations(potential_users, user.id)


def getRecommendations(users_df, uid):

    # Get the current user in the dataframe using their ID
    this_user = users_df.loc[users_df['user_id'] == uid]

    # calculate the similarity between this user and each other user in the dataframe
    for idx, row in users_df.iterrows():
        other_user = users_df.loc[users_df['user_id'] == row['user_id']]
        score = calculateSimilarities(this_user, other_user)
        users_df.at[idx, 'similarity_score'] = score

    # the current user will have the maximum similarity score, so we drop them from the dataframe
    u = users_df[users_df['user_id'] == uid].index
    users_df = users_df.drop(u)

    # if there is more than 100 recommendations, we only take the top 100
    # if there is less than 100, take whatever number of recommendations there are
    df_length = len(users_df['user_id'])
    if df_length > 100:
        recommendations_df = users_df.sort_values('similarity_score', ascending=False).head(100)
    else:
        recommendations_df = users_df.sort_values('similarity_score', ascending=False).head(df_length)

    return commitRecommendations(recommendations_df, uid)


# This method takes the user we are checking and the user who's recommendations are being calculated
# and individually identifies different similarities on each parameter: genres, instruments and band experience
def calculateSimilarities(_user, _other):

    # Genres are more important to the recommendation than instruments. For example a drummer who plays rock
    # would obviously prefer other musicians who play rock, not other drummers who play other genres
    gen_dist = distance.cosine(_user.iloc[0]['genres_data'], _other.iloc[0]['genres_data'])
    genre_score = (1 - gen_dist) * 2

    # Instruments similarity is similarly calculated, however using cosine_similarity which takes a 2D array
    # in contrast to the SciPy alternative which only takes a 1D array
    ins_dist = distance.cosine(_user.iloc[0]['instruments_data'], _other.iloc[0]['instruments_data'])
    exp_dist = distance.cosine(_user.iloc[0]['ins_exp_data'], _other.iloc[0]['ins_exp_data'])
    instrument_score = (1 - ins_dist) + (1 - exp_dist)

    # Band experience difference is calculated by dividing the lower number by the larger one and adding it to the score
    # For example, the user has 3 years band exp, the other has 8. 3/8 = .375
    # Or the user has 10 years exp, the other has 11. 10/11 = .909
    larger_num = max(_user.iloc[0]['band_data'], _other.iloc[0]['band_data'])
    lower_num = min(_user.iloc[0]['band_data'], _other.iloc[0]['band_data'])

    # if the numbers are the same, they have identical band experience
    if larger_num == lower_num:
        band_score = 1
    else:
        band_score = lower_num / larger_num

    # Instrument score divided by 4 as it is the least influential criteria
    score = genre_score + (instrument_score / 4) + band_score
    return score


# This function takes the recommendations dataframe and commits them to the database. If the user already
# had recommendations, it wipes these records and creates the new set
def commitRecommendations(dataframe, user_id):

    # Delete any records for this user if there are any present
    user = User.objects.get(id=user_id)
    UserRecommendation.objects.filter(user=user).delete()

    # Create the new records for each recommendation
    for idx, row in dataframe.iterrows():
        UserRecommendation.objects.create(
            user=user,
            recommendation=User.objects.get(id=row['user_id']),
            distance_from_user=row['distance_to_user'],
            score=row['similarity_score']
        )


dataPreProcessing(29600)

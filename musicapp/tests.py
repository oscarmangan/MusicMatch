from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from musicapp.models import *
from rest_framework.authtoken.models import Token

####################
#   API Testing    #
####################


class APIMainTestClass(APITestCase):

    # method to setup model instances for testing the API
    def setUp(self):
        user = User.objects.create(id=4, username='test_person')
        Profile.objects.create(
            user=User.objects.get(id=4),
            age=30,
            band_exp=0
        )
        Genre.objects.create(id=1, genre_name='Rock')
        Genre.objects.create(id=2, genre_name='Traditional')
        Genre.objects.create(id=3, genre_name='Metal')
        Instrument.objects.create(id=1, instrument_name='Acoustic Guitar')
        Instrument.objects.create(id=2, instrument_name='Electric Guitar')
        Instrument.objects.create(id=3, instrument_name='Bass Guitar')

    def test_login_auth(self):

        # create a sample user and commit to Database
        user = User.objects.create(id=5, username='test_person2')
        user.set_password(raw_password='test_pw')
        Token.objects.create(user=user)
        user.save()

        data = {
            'username': 'test_person2',
            'password': 'test_pw'
        }

        id_check = User.objects.get(username='test_person2').id
        token_check = Token.objects.get(user=User.objects.get(username='test_person2')).key

        # test that the login functionality returns the ID and token of the user
        response = self.client.post('/auth/', data)
        res_data = response.json()
        self.assertEqual(res_data['id'], id_check)
        self.assertEqual(res_data['token'], token_check)

    def test_create_user(self):
        data = {
            "username": "test_person1",
            "email": "test_person@test.com",
            "password": "test_password1",
            "profile": {
                "age": "30",
                "band_exp": "5",
                "bio": "Test bio",
                "facebook_url": "https://www.facebook.com/testcase",
                "instagram_url": "https://www.instagram.com/testcase",
                "lat_long": "53.360675,-6.262291599999999",
                "distance_limit": "50",
                "music_url": "https://www.soundcloud.com/testcase",
                "town": "Dublin",
                "twitter_url": "https://www.twitter.com/testcase"
            },
            "instruments": [
                {"instrument": "1", "name": "Acoustic Guitar", "experience_level": "12"},
                {"instrument": "2", "name": "Electric Guitar", "experience_level": "9"}
            ],
            "genres": [
                {"genre": "1"},
                {"genre": "2"}
            ],
            "images": []
        }

        # Call the API with the data given above at the signup endpoint
        response = self.client.post("/api/signup/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):

        user_id = User.objects.get(username='test_person').id
        data = {
            "user_id": user_id,
            "profile": {
                "bio": "test bio change",
                "age": 31
            },
            "instruments": [
                    {"instrument": "2", "name": "Electric Guitar Guitar", "experience_level": "12"},
                    {"instrument": "3", "name": "Bass Guitar", "experience_level": "9"}
                ],
            "genres": [
                {"genre": "2"},
                {"genre": "3"}
            ]
        }

        # test the update_user endpoint changing only certain elements of the profile
        response = self.client.patch("/update_user/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_recommendations(self):

        data = {"user_id": "4"}

        # test that the user can generate new recommendations just passing user id
        response = self.client.post("/set_recommendations/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_top_recommendations(self):

        # test that the client can retrieve their top recommendations
        response = self.client.get('/get_recommendations/', {'id': '4', 'limit': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_recommendations(self):

        # test that the client can retrieve all recommendations
        response = self.client.get('/get_recommendations/', {'id': '4', 'limit': 'false'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_user(self):

        # test to retrieve a specific user and all their associated details
        response = self.client.get("/api/users/4/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users(self):

        # test to retrieve all users and all their associated details
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_profiles(self):

        # test to retrieve all profiles in the database
        response = self.client.get("/api/profiles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_profile(self):
        # test to retrieve a specific profile
        user = User.objects.get(username='test_person')
        prof_id = Profile.objects.get(user=user).id
        url = "/api/profiles/" + str(prof_id) + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_genre(self):

        # test to retrieve a specific genre
        response = self.client.get("/api/genres/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_genres(self):

        # test to retrieve all genres
        response = self.client.get("/api/genres/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_instrument(self):

        # test to retrieve specific instrument
        response = self.client.get("/api/instruments/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_instruments(self):

        # test to retrieve all instruments
        response = self.client.get("/api/instruments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

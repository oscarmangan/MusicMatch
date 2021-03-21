from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from musicapp.serializers import *
from django.contrib.auth.models import User
from musicapp.models import Profile, Instrument, Genre, UserInstrument, UserGenre, UserRecommendation
import musicapp.recommenderSystem as rs


# ViewSets for all model serializers below
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication, )


# ViewSet for creating a new user instance
class CreateUserViewSet(viewsets.ModelViewSet):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    # POST request to CreateUserViewSet where we create a new account
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "User created successfully",
                             "id": serializer.instance.id}, status=status.HTTP_201_CREATED)
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


# Custom view to return the users ID along with their token when they log in
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class CreateUserImageViewSet(viewsets.ModelViewSet):
    serializer_class = CreateUserImageSerializer
    queryset = UserImage.objects.all()

    # POST request to CreateUserImageViewSet where we create a new account
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        user = request.data['user']
        images = dict(request.data.lists())['images']
        new_data = {'user': user, 'images': images}
        for i in range(len(new_data['images'])):
            new_data['images'][i] = {'image_file': new_data['images'][i]}

        serializer = CreateUserImageSerializer(data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Users images uploaded"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View class used to check if the username or email entered by the user in the first
# registration step has already been taken in the database
class CheckUserExists(APIView):

    # Function to check if the username or email input by the user exists in registration
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            name_to_check = request.data['username']
            email_to_check = request.data['email']
            # If username or email exists, then return true, which will
            # prevent user using that username or that email
            if User.objects.filter(email=email_to_check, username=name_to_check).exists():
                return Response({'email_username': True}, status=406)
            elif User.objects.filter(username=name_to_check).exists():
                return Response({'username': True}, status=406)
            elif User.objects.filter(email=email_to_check).exists():
                return Response({'email': True}, status=406)
            else:
                return Response({'pass': True}, status=200)
        except Exception as e:
            return Response({'message': str(e)}, status=400)


# View to take the users ID and set their recommendations based on their profile
class SetUserRecommendationsView(APIView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            user_id = request.data['user_id']
            # ensuring the users ID exists in the database before executing
            if User.objects.filter(id=user_id).exists():
                rs.dataPreProcessing(user_id)
                return Response({"status": "User recommendations generated"}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': "User not found"}, status=404)
        except Exception as e:
            return Response({'message': str(e)}, status=400)


# View class to get the recommendations for the user through serializer to display
class GetUserRecommendationsView(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET['id']
        limit = request.GET['limit']
        try:
            user = User.objects.get(id=user_id)
            # if the limit param is true, then we only want the first 9 recommendations
            if limit == "true":
                rec_list = UserRecommendation.objects.filter(user=user)[:9]
            else:
                rec_list = UserRecommendation.objects.filter(user=user)
            serializer = UserRecommendationsSerializer(rec_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=400)


# View to allow the user to update multiple models related to the user at once
class UpdateUserView(APIView):

    # patch request as the user only updates part of the overall collection of models
    def patch(self, request):
        user = User.objects.get(id=request.data['user_id'])
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

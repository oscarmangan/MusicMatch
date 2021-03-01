from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from musicapp.serializers import *
from django.contrib.auth.models import User
from musicapp.models import Profile, Instrument, Genre, UserInstrument, UserGenre


# ViewSets for all model serializers below
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication, )


class CreateUserViewSet(viewsets.ModelViewSet):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    # POST request to CreateUserViewSet where we create a new account
    @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
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


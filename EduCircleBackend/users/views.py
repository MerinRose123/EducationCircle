import jwt
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.signals import user_logged_in

from EduCircleBackend import settings
from users.serializers import UserSerializer
from users.models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):

    try:
        email = request.data['email']
        password = request.data['password']

        userdb = User.objects.get(email=email)
        credentials = {
            "email": email, "password": password
        }
        user = authenticate(request,**credentials)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                login(request, user)
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            return Response({'message': 'Can not authenticate with the given credentials or the account has been deactivated'},\
                                status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(request.user)
        content = {'message': 'Hello, World!'}
        return Response(content)


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Params: {
            "email": sacf,
            "first_name":sdf,
            "last_name":sdfkh,
            "password":sdfg
        }
        """
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveAPIView, GenericAPIView, DestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer, UserListSerializer
from users.models import User
from users.utils import validate_user_based_on_uid

# Initialize logger
logger = logging.getLogger(__name__)

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
                token = str(RefreshToken.for_user(user).access_token)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_details["id"] = user.id
                user_details["email"] = user.email
                user_details["username"] = user.username
                user_details["profile_image"] = user.profile_image if user.profile_image else ""
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


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,)

    def post(self, request):
        """
        Params: {
            "email": sacf,
            "first_name":sdf,
            "last_name":sdfkh,
            "password":sdfg
            "profile_image": <profile_image>
        }
        """
        user = request.data
        serializer = UserSerializer(data=user, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request, *args, **kwargs):
        try:
            user_id =  request.GET.get('user_id', None)
            user_instance = User.objects.get(id=user_id)
            serializer = self.serializer_class(user_instance, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('Error in UserRetrieveUpdateAPIView.Error - {}'.format(str(e)))
            raise ValidationError(e, 400)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data
        user_id =  request.GET.get('user_id', None)
        user_instance = User.objects.get(id=user_id)

        serializer = UserSerializer(
            instance = user_instance, data=serializer_data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    
class UserListView(ListAPIView):
    """
    Model view to list the users
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = UserListSerializer

    def get_queryset(self):
        """
        List atmost 30 news entries as latest first.
        """
        queryset = User.objects.filter().order_by('-created_at')[:30]
        return queryset

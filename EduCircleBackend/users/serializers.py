from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'created_at', 'password', 'profile_image')
        extra_kwargs = {'password': {'write_only': True}}
from rest_framework import serializers
from.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'created_at', 'password')
        extra_kwargs = {'password': {'write_only': True}}
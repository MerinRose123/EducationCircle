from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    # photo = serializers.SerializerMethodField()

    # def get_photo(self, instance):
    #     request = self.context['request']
    #     print(instance)
    #     if instance.profile_image:
    #         photo_url = instance.profile_image.url
    #         complete_photo_url = request.build_absolute_uri(photo_url)
    #     else:
    #         complete_photo_url = ''
    #     return complete_photo_url

    from django.contrib.auth.hashers import make_password


    def create(self, validated_data):

        if validated_data['username'] is None:
            raise TypeError('Users must have a username.')

        if validated_data['email'] is None:
            raise TypeError('Users must have an email address.')

        user = User.objects.create(
        email=validated_data['email'],
        username=validated_data['username'],
        profile_image=validated_data['profile_image'] if 'profile_image' in validated_data else None,
        last_name=validated_data['last_name'] if 'last_name' in validated_data else '',
        first_name=validated_data['first_name'] if 'first_name' in validated_data else '',
        password = make_password(validated_data['password']))

        return user

    class Meta(object):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'created_at', 'password', 'profile_image')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)


class UserListSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id', 'email', 'username')
        read_only_fields = ('id',)
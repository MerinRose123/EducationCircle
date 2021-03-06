from rest_framework import serializers
from users.models import User


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
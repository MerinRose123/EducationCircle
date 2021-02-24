from rest_framework import serializers

from common.models import FeedBack, Complaint


class FeedBackSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = FeedBack
        fields = ('created_by', 'rating', 'title', 'description')


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Complaint
        fields = ('created_by', 'targeted_user', 'title', 'description')
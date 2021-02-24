from rest_framework import serializers

from common.models import FeedBack, Complaint, News


class FeedBackSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = FeedBack
        fields = ('created_by', 'rating', 'title', 'description')


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Complaint
        fields = ('created_by', 'targeted_user', 'title', 'description')

    
class NewsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = News
        fields = ('created_by', 'site_link', 'title', 'description')
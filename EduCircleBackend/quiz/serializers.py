from rest_framework import serializers

from quiz.models import TestTaker, Test, Question, ExamType, Category


class CatgorySerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Category
        fields = ('title', 'key', 'description')


class ExamTypeSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = ExamType
        fields = ('title', 'key', 'description', 'site_link', 'community_leader')

class TestYearSerializer(serializers.ModelSerializer):
    """
    Retrieves the yearwise test ids for a particular exam type
    """

    class Meta(object):
        model = Test
        fields = ('id', 'title', 'year')
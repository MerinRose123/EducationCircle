from rest_framework import serializers

from common.models import FeedBack, Complaint, News, DiscussionQuestion, Answer


class FeedBackSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = FeedBack
        fields = ('id', 'created_by', 'rating', 'title', 'description')


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Complaint
        fields = ('id', 'created_by', 'targeted_user', 'title', 'description')

    
class NewsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = News
        fields = ('id', 'created_by', 'site_link', 'title', 'description')


class DiscussionQuestionSerializer(serializers.ModelSerializer):
    created_by_username = serializers.SerializerMethodField()
    exam_type_key = serializers.SerializerMethodField()
    exam_type_title = serializers.SerializerMethodField()

    def get_created_by_username(self, instance):
        return instance.created_by.username
    
    def get_exam_type_key(self, instance):
        return instance.exam_type.key

    def get_exam_type_title(self, instance):
        return instance.exam_type.title

    class Meta(object):
        model = DiscussionQuestion
        fields = ('id', 'created_by', 'question_text', 'title', 'exam_type_key', 'exam_type_title', 'exam_type', 'created_by_username')


class DiscussionAnswerSerializer(serializers.ModelSerializer):
    created_by_username = serializers.SerializerMethodField()

    def get_created_by_username(self, instance):
        return instance.created_by.username

    class Meta(object):
        model = Answer
        fields = ('id', 'created_by', 'text', 'title', 'created_by_username', 'question')
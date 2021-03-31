from rest_framework import serializers

from quiz.models import TestTaker, Test, Question, ExamType, Category


class CatgorySerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Category
        fields = ('id', 'title', 'key', 'description')


class ExamTypeSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = ExamType
        fields = ('id', 'title', 'key', 'description', 'site_link', 'community_leader')

class TestYearSerializer(serializers.ModelSerializer):
    """
    Retrieves the yearwise test ids for a particular exam type
    """

    class Meta(object):
        model = Test
        fields = ('id', 'title', 'year', 'paper_type', 'no_questions')

    
class MockTestSerializer(serializers.ModelSerializer):
    """
    Retrieves the mock test ids for a particular exam type
    """

    class Meta(object):
        model = Test
        fields = ('id', 'title', 'paper_type', 'no_questions')


class CategoryTestSerializer(serializers.ModelSerializer):
    """
    Retrieves the test ids for a particular category
    """

    class Meta(object):
        model = Test
        fields = ('id', 'title', 'paper_type', 'no_questions', 'category')


class QuestionSerilaizer(serializers.ModelSerializer):

    categories = serializers.SerializerMethodField()

    def get_categories(self, instance):
        return CatgorySerializer(Category.objects.filter(category=instance), many=True).data

    class Meta(object):
        model = Question
        fields = ('id', 'title', 'question_text', 'question_type', 'choice1', 
        'choice2', 'choice3', 'choice4', 'answer', 'description', 'categories')


class TestSerializer(serializers.ModelSerializer):
    """
    Retrieves the test with questions
    """
    questions = serializers.SerializerMethodField()

    def get_questions(self, instance):
        return QuestionSerilaizer(Question.objects.filter(question_test=instance), many=True).data

    class Meta(object):
        model = Test
        fields = ('id', 'title', 'paper_type', 'no_questions', 'category', 'year', 'questions')


class TestTakerSerializer(serializers.ModelSerializer):
    """
    Saves a test result
    """

    class Meta(object):
        model = TestTaker
        fields = ('id', 'description', 'user', 'test', 'score', 'total_score', 'percentage', 'completed')


class TestResultSerializer(serializers.ModelSerializer):
    """
    Gets all test results of a user
    """
    test_name = serializers.SerializerMethodField()
    paper_type = serializers.SerializerMethodField()
    test_type_name = serializers.SerializerMethodField()
    test_type_id = serializers.SerializerMethodField()

    def get_test_name(self, instance):
        return instance.test.title

    def get_paper_type(self, instance):
        return instance.test.paper_type

    def get_test_type_name(self, instance):
        if instance.test.exam_type:
            return instance.test.exam_type.title
        return instance.test.category.title

    def get_test_type_id(self, instance):
        if instance.test.exam_type:
            return instance.test.exam_type.id
        return instance.test.category.id

    class Meta(object):
        model = TestTaker
        fields = ('id', 'description', 'test', 'score', 'total_score', 'percentage', 
            'completed', 'test_name', 'paper_type', 'test_type_name', 'test_type_id')
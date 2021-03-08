from django.shortcuts import render
import logging

from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveAPIView, \
    GenericAPIView, DestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from quiz.serializers import CatgorySerializer, ExamTypeSerializer, TestYearSerializer, MockTestSerializer, \
    CategoryTestSerializer, TestSerializer, TestTakerSerializer, TestResultSerializer
from quiz.models import Category, ExamType, Test, TestTaker

# Initialize logger
logger = logging.getLogger(__name__)


class CategoryListView(ListAPIView):
    """
    Model view to list the categories
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = CatgorySerializer

    def get_queryset(self):
        """
        List categories
        """
        queryset = Category.objects.filter().all()
        return queryset


class ExamTypeListView(ListAPIView):
    """
    Model view to list the exam type
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = ExamTypeSerializer

    def get_queryset(self):
        """
        List exam types
        """
        queryset = ExamType.objects.filter().all()
        return queryset
    

class ExamYearRetrieveView(ListAPIView):
    """
    Retrieves the available years for the question papers for a particular exam type.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = TestYearSerializer

    def get_queryset(self, *args, **kwargs):
        """
        retrieves the available years for the question papers for a particular exam type.
        """
        type_key = self.request.GET.get('exam_type', 'ssc')
        exam_type = ExamType.objects.filter(key=type_key).first()
        queryset = Test.objects.filter(exam_type=exam_type, paper_type='prev_year').all().order_by('year')
        return queryset


class MockTestRetrieveView(ListAPIView):
    """
    Retrieves the available mock tests for a particular exam type.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = MockTestSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Retrieves the available mock tests for a particular exam type.
        """
        type_key = self.request.GET.get('exam_type', 'ssc')
        exam_type = ExamType.objects.filter(key=type_key).first()
        queryset = Test.objects.filter(exam_type=exam_type, paper_type="mock_test").all().order_by('-created_at')
        return queryset

class CategoryTestRetrieveView(ListAPIView):
    """
    Retrieves the available tests for a particular category
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = MockTestSerializer

    def get_queryset(self, *args, **kwargs):
        """
         Retrieves the available tests for a particular category
        """
        type_key = self.request.GET.get('category', 'current_affairs')
        category = Category.objects.filter(key=type_key).first()
        queryset = Test.objects.filter(category=category, paper_type="quiz").all().order_by('-created_at')
        return queryset


class TestRetrieveView(ListAPIView):
    """
    Retrieve a test with all questions by id
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = TestSerializer

    def get(self, request, *args, **kwargs):
        try:
            test_id = self.request.GET.get('test_id', None)
            test_instance = Test.objects.get(id=test_id)
            serializer = self.serializer_class(test_instance, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('Error in TestRetrieveView.Error - {}'.format(str(e)))
            raise ValidationError(e, 400)


class TestResultView(GenericAPIView):
    """
    To save a test result in a user specific manner .
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = TestTakerSerializer

    def post(self, request, *args, **kwargs):
        """
        To save a test result in a user specific manner
        """
        try:
            serializer_data = {
                'user': request.user.id,
                'test': request.data['test'],
                'score': request.data['score'],
                'total_score': request.data['total_score'],
                'completed': request.data.get('completed', True),
                'percentage': int(request.data['score'] * 100/ request.data['total_score'])
            }

            serializer = self.get_serializer(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "Result saved succesfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('Error in TestResultView.Error - {}'.format(str(e)))
            raise ValidationError(e, 400)


class TestResultGetView(ListAPIView):
    """
    Retrieve all test results of a user.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = TestResultSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Retrieve all test results of a user.
        """
        queryset = TestTaker.objects.filter(user=self.request.user).all().order_by('-created_at')
        return queryset
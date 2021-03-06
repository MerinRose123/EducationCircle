import logging

from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveAPIView, \
    GenericAPIView, DestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from common import constants as common_constants
from common.serializers import FeedBackSerializer, ComplaintSerializer, NewsSerializer, \
    DiscussionQuestionSerializer, DiscussionAnswerSerializer
from common.models import News, DiscussionQuestion, Answer
from quiz.models import ExamType

# Initialize logger
logger = logging.getLogger(__name__)


class FeedbackView(GenericAPIView):
    """
    Model view to send feedback to educircle support when user gives feedback data.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = FeedBackSerializer

    def post(self, request, *args, **kwargs):
        """
        POST to send feed back to educircle support.

        :param request: The WSGI request instance
        :param args:
        :param kwargs:
        :return: Success message
        """

        try:
            serializer_data = {
                'created_by': request.user.id,
                'description': request.data['description'],
                'title': request.data['title'],
                'rating': request.data['rating']
            }

            serializer = self.get_serializer(data=serializer_data)

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": common_constants.FEEDBACK_SEND_SUCCESSFULLY}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('Error in FeedbackView.Error - {}'.format(str(e)))
            raise ValidationError(e, 400)


class ComplaintView(GenericAPIView):
    """
    Model view to send compliant to educircle
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = ComplaintSerializer

    def post(self, request, *args, **kwargs):
        """
        POST to send compliant to educircle

        :param request: The WSGI request instance
        :param args:
        :param kwargs:
        :return: Success message
        """

        try:
            serializer_data = {
                'created_by': request.user.id,
                'description': request.data['description'],
                'title': request.data['title'],
                'targeted_user': request.data['targeted_user_id']
            }

            serializer = self.get_serializer(data=serializer_data)

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": common_constants.COMPLAINT_SEND_SUCCESSFULLY}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('Error in ComplaintView.Error - {}'.format(str(e)))
            raise ValidationError(e, 400)


class NewsListView(ListAPIView):
    """
    Model view to list the latest news
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = NewsSerializer

    def get_queryset(self):
        """
        List atmost 20 news entries as latest first.
        """
        queryset = News.objects.filter().order_by('-created_at')[:20]
        return queryset

# Discussion platform related
class CreateQuestionAPIView(GenericAPIView):
    
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """
        Params: {
            "created_by": "bdcbd239-619c-4b6c-9ec2-6c73c3d9a66b",
            "question_text": "What are the topics for SSC",
            "title": "SSC Topics",
            "exam_type": "701707ed-3516-4faa-a5bb-106178268410"
        }
        """
        data = request.data
        serializer = DiscussionQuestionSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateAnswerAPIView(GenericAPIView):
    
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """
        Params: {
            "title"
            "text"
            "question"
        }
        """
        data = request.data
        serializer = DiscussionAnswerSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DiscussionQuestionListView(ListAPIView):
    """
    List questions
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = DiscussionQuestionSerializer

    def get_queryset(self, *args, **kwargs):
        """
        List questions
        """
        type_key = self.request.GET.get('exam_type', 'ssc')
        exam_type = ExamType.objects.filter(key=type_key).first()
        queryset = DiscussionQuestion.objects.filter(exam_type=exam_type).all().order_by('-created_at')
        return queryset

class DiscussionAnswerListView(ListAPIView):
    """
    List questions
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = DiscussionAnswerSerializer

    def get_queryset(self, *args, **kwargs):
        """
        List questions
        """
        question_id = self.request.GET.get('question_id', None)
        question = DiscussionQuestion.objects.filter(id=question_id).first()
        queryset = Answer.objects.filter(question=question).all().order_by('-created_at')
        return queryset
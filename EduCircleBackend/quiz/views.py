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

from quiz.serializers import CatgorySerializer, ExamTypeSerializer, TestYearSerializer
from quiz.models import Category, ExamType, Test


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

    def get(self, request, *args, **kwargs):
        """
        retrieves the available years for the question papers for a particular exam type.
        """
        print(self.request)
        exam_type = self.request.args.get('exam_type', 'SSC')
        exam_type = 'SSC'
        queryset = Test.objects.filter(exam_type=exam_type, paper_type='prev_year').all().order_by('year')
        return queryset
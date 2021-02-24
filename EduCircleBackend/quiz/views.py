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

from quiz.serializers import CatgorySerializer, ExamTypeSerializer
from quiz.models import Category, ExamType


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
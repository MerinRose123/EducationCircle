from django.contrib import admin
from django.urls import path, include

from common.views import FeedbackView, ComplaintView

urlpatterns = [
     path('feedback', FeedbackView.as_view(), name='post_feedback'),
     path('complaint', ComplaintView.as_view(), name='post_complaint'),
]
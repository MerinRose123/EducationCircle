from django.contrib import admin
from django.urls import path, include

from common.views import FeedbackView, ComplaintView, NewsListView

urlpatterns = [
     path('feedback', FeedbackView.as_view(), name='post_feedback'),
     path('complaint', ComplaintView.as_view(), name='post_complaint'),
     path('news_list', NewsListView.as_view(), name='list_news'),
]
from django.contrib import admin
from django.urls import path, include

from common.views import FeedbackView, ComplaintView, NewsListView, CreateQuestionAPIView, CreateAnswerAPIView, \
      DiscussionQuestionListView, DiscussionAnswerListView

urlpatterns = [
     path('feedback', FeedbackView.as_view(), name='post_feedback'),
     path('complaint', ComplaintView.as_view(), name='post_complaint'),
     path('news-list', NewsListView.as_view(), name='list_news'),

     # Discussion platform/ community related
     path('post-question', CreateQuestionAPIView.as_view(), name='post-discussion-question'),
     path('post-answer', CreateAnswerAPIView.as_view(), name='post-discussion-answer'),
     path('question-list', DiscussionQuestionListView.as_view(), name='question-list'),
     path('answer-list', DiscussionAnswerListView.as_view(), name='answer-list'),
]
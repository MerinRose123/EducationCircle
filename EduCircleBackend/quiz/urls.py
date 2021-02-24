from django.urls import path

from quiz.views import CategoryListView, ExamTypeListView

urlpatterns = [
    path('category_list', CategoryListView.as_view(), name='list_category'),
    path('exam_type_list', ExamTypeListView.as_view(), name='exam_type_list'),
]
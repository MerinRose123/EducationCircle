from django.urls import path

from quiz.views import CategoryListView, ExamTypeListView, ExamYearRetrieveView

urlpatterns = [
    path('category_list', CategoryListView.as_view(), name='list_category'),
    path('exam_type_list', ExamTypeListView.as_view(), name='exam_type_list'),
    path('year_list', ExamYearRetrieveView.as_view(), name='type_year_list'),
]
from django.urls import path

from quiz.views import CategoryListView, ExamTypeListView, ExamYearRetrieveView

urlpatterns = [
    path('category-list', CategoryListView.as_view(), name='list_category'),
    path('exam-type-list', ExamTypeListView.as_view(), name='exam_type_list'),
    path('year-list', ExamYearRetrieveView.as_view(), name='type_year_list'),
]
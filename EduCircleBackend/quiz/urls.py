from django.urls import path

from quiz.views import CategoryListView, ExamTypeListView, ExamYearRetrieveView, MockTestRetrieveView, \
    CategoryTestRetrieveView, TestRetrieveView, TestResultView, TestResultGetView

urlpatterns = [
    path('category-list', CategoryListView.as_view(), name='list_category'),
    path('exam-type-list', ExamTypeListView.as_view(), name='exam_type_list'),
    path('year-list', ExamYearRetrieveView.as_view(), name='type_year_list'),
    path('mock-test-list', MockTestRetrieveView.as_view(), name='mock-test_list'),
    path('category-test-list', CategoryTestRetrieveView.as_view(), name='category-test-list'),
    path('get-test', TestRetrieveView.as_view(), name='get-test'),
    path('save-test', TestResultView.as_view(), name='save-test'),
    path('get-results', TestResultGetView.as_view(), name='get-test-results'),
]
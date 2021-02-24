from django.urls import path
# from rest_framework_simplejwt import views as jwt_views
from .views import CreateUserAPIView, UserRetrieveUpdateAPIView, authenticate_user

urlpatterns = [
    path('token', authenticate_user),
    path('register', CreateUserAPIView.as_view(), name='register_user'),
    path('manage', UserRetrieveUpdateAPIView.as_view(), name='retrieve_or_update_user'),
]
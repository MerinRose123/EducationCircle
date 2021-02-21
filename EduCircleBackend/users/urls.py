from django.urls import path
# from rest_framework_simplejwt import views as jwt_views
from .views import HelloView, CreateUserAPIView, UserRetrieveUpdateAPIView, authenticate_user

urlpatterns = [
    path('api/token/', authenticate_user),
    path('api/hello/', HelloView.as_view(), name='hello'),
    path('api/user/register', CreateUserAPIView.as_view(), name='register_user'),
    path('api/user/manage', UserRetrieveUpdateAPIView.as_view(), name='retrieve_or_update_user'),
]
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import user_signup,celebrity_signup,user_login, celebrity_login

urlpatterns = [
    path('signup/',user_signup,name='user-signup'),
    path('celebrity/signup/',celebrity_signup,name='celebrity-signup'),
    path('login/', user_login, name='user-login'),
    path('celebrity/login/', celebrity_login, name='celebrity-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh')
]

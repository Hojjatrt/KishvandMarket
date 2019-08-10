from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from userapp.api.views import *

urlpatterns = [
    path('token-auth/', obtain_auth_token, name='api_token_auth'),
    path('signup/', Signup.as_view(), name='signup_api'),
]

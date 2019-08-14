from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from userapp.api.views import *

urlpatterns = [
    path('token-auth/', obtain_auth_token, name='api_token_auth'),
    path('signup/', Signup.as_view(), name='signup_api'),
    path('verify/', Verify.as_view(), name='verify_api'),
    path('login/', Login.as_view(), name='login_api'),
    path('update-user/', UserUpdate.as_view(), name='update_user_api'),
]

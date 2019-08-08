from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from userapp.api import views

urlpatterns = [
    path('api/', include('userapp.api.urls'), name='user_api'),
]

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path(r'products/', ProductListAPIView.as_view(), name='products'),
    path(r'maincategories/', MainCategoryListAPIView.as_view(), name='maincategories'),
    path(r'subcategories/', SubCategoryListAPIView.as_view(), name='subcategories'),
]

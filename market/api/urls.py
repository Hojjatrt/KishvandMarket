from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='products'),
    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='Product'),
    path('maincategories/', MainCategoryListAPIView.as_view(), name='maincategories'),
    path('subcategories/', SubCategoryListAPIView.as_view(), name='subcategories'),
    path('times/', TimeListAPIView.as_view(), name='time services'),
    path('times/<str:day>/', TimeListAPIView.as_view(), name='time services'),
    path('slides/', SlideAPIView.as_view(), name='Slides'),
    path('check-products/', CartProductsAPIView.as_view(), name='Check CartProducts'),
    path('cart/', CartAPIView.as_view(), name='Cart'),
    path('cart/<int:id>/', CartDetailAPIView.as_view(), name='Cart Detail'),
    path('cart-list/', CartListAPIView.as_view(), name='Cart list'),
]

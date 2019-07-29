from rest_framework import generics
from rest_framework.filters import SearchFilter
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from market.models import *
from .serializers import *

##################
##################

@method_decorator(csrf_exempt, name='dispatch')
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('id') # Q(status = 1) | Q(status = 3))
    serializer_class = ProductListSerializer
    filter_backends = (SearchFilter,)
    filter_fields = ('category',)
    search_fields = ('name', 'category__title')
    # permission_classes = (IsClient,)
    # pagination_class = LargePagesPagination

##################
##################

@method_decorator(csrf_exempt, name='dispatch')
class CategoryListAPIView(generics.ListAPIView):
    queryset = MainCategory.objects.all().order_by('id')
    # authentication_classes = (TokenAuthentication,)
    serializer_class = CategoryListSerializer


@method_decorator(csrf_exempt, name='dispatch')
class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all().order_by('id')
    # authentication_classes = (TokenAuthentication,)
    serializer_class = SubCategoryListSerializer

##################
##################

@method_decorator(csrf_exempt, name='dispatch')
class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by('id')
    # authentication_classes = (TokenAuthentication,)
    serializer_class = TagListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from market.models import *
from .serializers import *


##################
##################

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['categories', 'min_price', 'max_price']


@method_decorator(csrf_exempt, name='dispatch')
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('id')  # Q(status = 1) | Q(status = 3))
    serializer_class = ProductListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    # filter_fields = ('categories',)
    # filterset_fields = ['categories',]
    filterset_class = ProductFilter
    search_fields = ('name', 'categories__title')
    # permission_classes = (IsClient,)
    pagination_class = SmallPagesPagination

    def get(self, request, *args, **kwargs):
        li = self.list(request, *args, **kwargs)
        res = Response(li.data, status=status.HTTP_200_OK)
        res['Access-Control-Allow-Origin'] = '*'
        return res


@method_decorator(csrf_exempt, name='dispatch')
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        ret = self.retrieve(request, *args, **kwargs)
        res = Response(ret.data, status=status.HTTP_200_OK)
        res['Access-Control-Allow-Origin'] = '*'
        return res

##################
##################


@method_decorator(csrf_exempt, name='dispatch')
class MainCategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = CategoryListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        res = Response(serializer.data, status=status.HTTP_200_OK)
        res['Access-Control-Allow-Origin'] = '*'
        return res


@method_decorator(csrf_exempt, name='dispatch')
class SubCategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=False)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = SubCategoryListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        res = Response(serializer.data, status=status.HTTP_200_OK)
        res['Access-Control-Allow-Origin'] = '*'
        return res

##################
##################


@method_decorator(csrf_exempt, name='dispatch')
class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by('id')
    # authentication_classes = (TokenAuthentication,)
    serializer_class = TagListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        res = Response(serializer.data, status=status.HTTP_200_OK)
        res['Access-Control-Allow-Origin'] = '*'
        return res

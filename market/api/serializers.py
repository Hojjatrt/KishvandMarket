from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import *
from market.models import *

##################
##################


class SmallPagesPagination(PageNumberPagination):
    page_size = 20


class LargePagesPagination(PageNumberPagination):
    page_size = 50

##################
##################

class CategoryListSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = Category
        fields = ('id', 'title', 'thumbnail', 'children', 'order')


class SubCategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'parent', 'order')


class SubCatProductSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title',)

##################
##################

class TagListSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class TagProductSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title',)

##################
##################

class ProductListSerializer(ModelSerializer):
    categories = SubCatProductSerializer(many=True)
    tags = StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = '__all__'

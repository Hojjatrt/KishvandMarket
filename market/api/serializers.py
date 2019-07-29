from rest_framework.serializers import ModelSerializer
from market.models import *


##################
##################

class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = MainCategory
        fields = ('id', 'title')


class SubCategoryListSerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'title', 'thumbnail', 'parent__title')

##################
##################

class ProductListSerializer(ModelSerializer):
    # category = CatProductSerializer()
    # producer = ProducerSerializer()

    class Meta:
        model = Product
        fields = '__all__'

##################
##################

class TagListSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


from django.http import HttpRequest
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import *
from market.models import *
from rest_framework import serializers

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


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)

##################
##################


class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

##################
##################


class ProductListSerializer(ModelSerializer):
    categories = SubCatProductSerializer(many=True)
    tags = StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        stock = Stock.objects.filter(product_id=instance.id).order_by('price').first()
        data = super(ProductListSerializer, self).to_representation(instance)
        data.update()
        if instance.thumb:
            data.update({
                "thumb": settings.BASE_URL + settings.MEDIA_URL + instance.thumb,
                "qnt": stock.qnt,
                "price": stock.price,
                "discount": stock.discount_ratio,
            })
        else:
            data.update({
                "thumb": instance.thumb,
                "qnt": stock.qnt,
                "price": stock.price,
                "discount": stock.discount_ratio,
            })
        return data


class ProductDetailSerializer(ModelSerializer):
    categories = SubCatProductSerializer(many=True)
    tags = StringRelatedField(many=True)
    images = ImageSerializer(many=True, source='image_set')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        stock = Stock.objects.filter(product_id=instance.id).order_by('price').first()
        data = super(ProductDetailSerializer, self).to_representation(instance)
        data.update()
        if instance.thumb:
            data.update({
                "thumb": settings.BASE_URL + settings.MEDIA_URL + instance.thumb,
                "qnt": stock.qnt,
                "price": stock.price,
                "discount": stock.discount_ratio,
            })
        else:
            data.update({
                "thumb": instance.thumb,
                "qnt": stock.qnt,
                "price": stock.price,
                "discount": stock.discount_ratio,
            })
        return data

##################
##################


class TimeListSerializer(ModelSerializer):
    class Meta:
        model = Time
        fields = '__all__'

##################
##################


class SlideListSerializer(ModelSerializer):
    class Meta:
        model = Slide
        fields = '__all__'

##################
##################


class CartProductsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    qnt = serializers.IntegerField(required=True)


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    # amount = serializers.IntegerField(required=False)
    # address = serializers.CharField(max_length=150, required=False)
    products = serializers.CharField(required=False)
    number = serializers.IntegerField(required=False)


class CartListSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Cart
        fields = ('id', 'user', 'products')

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "code": instance.code,
            "user": instance.user.id,
            "status": instance.status,
            "products": instance.products,
        }

#########################
#########################

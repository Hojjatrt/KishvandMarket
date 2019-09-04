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


class CartProductsDetailSerializer(ModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    qnt = serializers.ReadOnlyField(source='number')

    class Meta:
        model = CartProduct
        fields = ('product_id', 'qnt')


class CartSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    time_id = serializers.IntegerField(required=True)
    address_id = serializers.IntegerField(required=True)
    date = serializers.CharField(required=False, max_length=15)
    products = CartProductsSerializer(required=True, many=True)
    # payment = serializers.IntegerField(required=False)


class CartListSerializer(ModelSerializer):
    time = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = ('id', 'code', 'date', 'status',
                  'time')


class CartDetailSerializer(ModelSerializer):
    time = serializers.StringRelatedField()
    products = CartProductsDetailSerializer(source='cartproduct_set', many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

#########################
#########################

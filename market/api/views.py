from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from market.models import *
from .serializers import *
import jdatetime


##################
##################

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['categories', 'min_price', 'max_price']


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
        return Response(li.data, status=status.HTTP_200_OK,
                        headers={'Access-Control-Allow-Origin': '*'})


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        ret = self.retrieve(request, *args, **kwargs)
        return Response(ret.data, status=status.HTTP_200_OK,
                        headers={'Access-Control-Allow-Origin': '*'})

##################
##################


class MainCategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = CategoryListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers={'Access-Control-Allow-Origin': '*'})


class SubCategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=False)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = SubCategoryListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers={'Access-Control-Allow-Origin': '*'})

##########################
##########################


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by('id')
    # authentication_classes = (TokenAuthentication,)
    serializer_class = TagListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers={'Access-Control-Allow-Origin': '*'})

##########################
##########################


class TimeListAPIView(generics.ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    serializer_class = TimeListSerializer

    def get_queryset(self):
        day = self.kwargs.get('day', '')
        now = jdatetime.datetime.now()
        now_t = now.time()
        now_d = now.date()
        if day == 'tomorrow':
            now_d = now_d + jdatetime.timedelta(days=1)
            now_t = jdatetime.time(5, 0)
        timefilter = ExcludeDate.objects.filter(Q(date=now_d) | Q(day=now_d.weekday()))
        timeservices = Time.objects.all().exclude(
            excludedate__in=timefilter
        )
        for t in timeservices:
            if t.strparse.hour <= now_t.hour:
                if t.strparse.hour == now_t.hour:
                    minutes = t.strparse.minute - now_t.minute
                    if minutes < 0:
                        minutes = minutes * -1
                    if minutes > 15:
                        timeservices = timeservices.exclude(pk=t.pk)
                else:
                    timeservices = timeservices.exclude(pk=t.pk)
        return timeservices.order_by('id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers={'Access-Control-Allow-Origin': '*'})

##########################
##########################


def check_products(products):
    li = []
    check = True
    amount = 0
    if products is None:
        check = False
    for p in products:
        dic = {}
        product_id = p.get('product_id', 0)
        qnt = p.get('qnt', 0)
        product = Product.objects.get(id=product_id)
        stock = Stock.objects.filter(product_id=product.id).order_by('price').first()
        dic['product_id'] = product.id
        dic['qnt'] = qnt
        amount += (qnt * (stock.price - (stock.price * stock.discount_ratio)))
        if qnt < stock.qnt:
            dic['status'] = 'ok'
        else:
            check = False
            dic['status'] = 'nok'
        li.append(dic)
    return li, check, amount


@method_decorator(csrf_exempt, name='dispatch')
class CartProductsAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = CartProductsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            try:
                user = request.user
                if user.is_anonymous:
                    content = {'code': 1, 'detail': 'user is anonymous.'}
                    return Response(content, status=status.HTTP_200_OK)

                try:
                    response_list = check_products(serializer.validated_data)[0]
                    content = {'code': 0, 'detail': response_list}
                    return Response(content, status=status.HTTP_200_OK,
                                    headers={'Access-Control-Allow-Origin': '*'})
                except Product.DoesNotExist:
                    content = {'code': 3, 'detail': 'This product not exist'}
                    return Response(content, status=status.HTTP_200_OK,
                                    headers={'Access-Control-Allow-Origin': '*'})

            except:
                content = {'code': 2, 'detail': 'error occurred in cartProduct api view.'}
                return Response(content, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class CartAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = CartSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
                if user.is_anonymous:
                    content = {'code': 1, 'detail': 'user is anonymous.'}
                    return Response(content, status=status.HTTP_200_OK)
                try:
                    products = serializer.validated_data.get('products', None)
                    response_list, check, main_amount = check_products(products)
                    if not check:
                        content = {'code': 1, 'status': 'nok', 'detail': response_list}
                        return Response(content, status=status.HTTP_200_OK,
                                        headers={'Access-Control-Allow-Origin': '*'})
                    time_id = serializer.validated_data.get('time_id', 0)
                    address_id = serializer.validated_data.get('address_id', 0)
                    amount = serializer.validated_data.get('amount', 0)
                    date = serializer.validated_data.get('date', None)
                    if date is None:
                        date = jdatetime.datetime.now().date()
                    elif date == 'tomorrow':
                        date = jdatetime.datetime.now().date() + jdatetime.timedelta(days=1)
                    # payment = serializer.validated_data.get('payment', 0)
                    time = Time.objects.get(id=time_id)
                    address = Address.objects.get(id=address_id, user=user)
                    if amount != main_amount:
                        content = {'code': 4, 'detail': 'amount is not equal with server\'s amount'}
                        return Response(content, status=status.HTTP_200_OK,
                                        headers={'Access-Control-Allow-Origin': '*'})
                    cart = Cart.objects.create(time=time, address=address, amount=amount, customer=user,
                                               date=date)
                    for p in products:
                        product_id = p.get('product_id', 0)
                        qnt = p.get('qnt', 0)
                        CartProduct.objects.create(cart_id=cart.id, product_id=product_id, number=qnt)

                    content = {'code': 0, 'id': cart.id, 'date': date, 'time': time.id, 'amount': main_amount,
                               'status': cart.status, 'payment': cart.pay_method}
                    return Response(content, status=status.HTTP_200_OK,
                                    headers={'Access-Control-Allow-Origin': '*'})

                except Product.DoesNotExist:
                    content = {'code': 3, 'detail': 'This product is not exist'}
                    return Response(content, status=status.HTTP_200_OK,
                                    headers={'Access-Control-Allow-Origin': '*'})
                except Time.DoesNotExist:
                    content = {'code': 5, 'detail': 'This time is not exist'}
                    return Response(content, status=status.HTTP_200_OK,
                                    headers={'Access-Control-Allow-Origin': '*'})
                except Address.DoesNotExist:
                    content = {'code': 6, 'detail': 'This address is not exist'}
                    return Response(content, status=status.HTTP_200_OK,
                                    headers={'Access-Control-Allow-Origin': '*'})
            except:
                content = {'code': 2, 'detail': 'error occurred in cart api view.'}
                return Response(content, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_200_OK)


class CartListAPIView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = CartListSerializer

    def get_queryset(self):
        queryset = Cart.objects.all().order_by('id')
        queryset = queryset.filter(customer=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers={'Access-Control-Allow-Origin': '*'})

##########################
##########################


class SlideAPIView(generics.ListAPIView):
    queryset = Slide.objects.all().order_by('id')
    # authentication_classes = (TokenAuthentication,)
    serializer_class = SlideListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers={'Access-Control-Allow-Origin': '*'})

##########################
##########################

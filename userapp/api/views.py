import binascii
import os
import jdatetime
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from userapp.api.serializers import *
from userapp.models import *
from userapp.api.permissions import *
from rest_framework.authtoken.models import Token


def _generate_pass():
    return binascii.hexlify(os.urandom(20))


class Signup(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            check_sms_or_call = False
            must_validate_sms = getattr(settings, "AUTH_SMS_VERIFICATION", True)

            try:
                user = get_user_model().objects.get(phone=phone)
                signup_sms_code = VerifyCode.objects.filter(user=user).last()
                if signup_sms_code is not None:
                    now = jdatetime.datetime.now()

                    # for i in signup_sms_code:
                    c = signup_sms_code.created_at

                    sub = (now-c).total_seconds()
                    if sub < 0:
                        sub = sub * -1
                    if sub <= 120:
                        content = {
                            'code': 2,
                            'status': 'no',
                            'detail': '2 mins ago you have a sms'
                            }
                        return Response(content, status=status.HTTP_200_OK)
                    signup_sms_code.delete()

            except VerifyCode.DoesNotExist:
                pass

            except get_user_model().DoesNotExist:
                try:
                    user = get_user_model().objects.create_user(username=phone, phone=phone)
                    user.is_active = False
                    check_sms_or_call = True
                except:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Set user fields provided
            # if not user.is_active:
            #     password = _generate_pass()
            #     user.set_password(password)

            user.save()
            if must_validate_sms:
                # Create and associate signup code
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '0.0.0.0')
                if x_forwarded_for:
                    ipaddr = x_forwarded_for.split(',')[0]
                else:
                    ipaddr = request.META.get('REMOTE_ADDR', '0.0.0.0')

                signup_sms_code = VerifyCode.objects.create_sms_code(user=user, ipaddr=ipaddr)
                check_status = signup_sms_code.send_signup_sms()
                # TODO : check this status after get code
                if not check_status:
                    print("check status in sms error phone is : ", user.phone)
                    content = {'code': 1,
                               'status': 'no'
                               }
                else:
                    content = {'code': 0,
                               'status': 'ok'
                               }
            return Response(content, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

############################
############################


class Verify(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifySerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            verified = False
            code = serializer.validated_data['code']
            phone = serializer.validated_data['phone']
            try:
                user = get_user_model().objects.get(phone=phone)
            except get_user_model().DoesNotExist:
                content = {'code': 1, 'status': 'no', 'detail': 'user does not exist.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            try:
                verified = VerifyCode.objects.set_user_is_verified(code=code, user=user)
            except VerifyCode.DoesNotExist:
                content = {'code': 2, 'status': 'no', 'detail': 'code does not exist.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            if verified:
                content = {'code': 0, 'status': 'ok', 'detail': 'User verified.'}
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {'code': 3, 'status': 'no', 'detail': 'Unable to verify user.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

############################
############################


class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            try:
                user = get_user_model().objects.get(phone=phone)
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'code': 0, 'id': user.id, 'token': token.key, 'fname': user.first_name,
                                     'lname': user.last_name, 'email': user.email},
                                    status=status.HTTP_200_OK)
                else:
                    content = {'code': 2, 'detail': 'Unable to login with provided credentials.'}
                    return Response(content, status=status.HTTP_202_ACCEPTED)
            except get_user_model().DoesNotExist:
                return Response({'code': 3, 'detail': 'user does not exist.'}, status=status.HTTP_202_ACCEPTED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

############################
############################


class UserUpdate(APIView):
    permission_classes = IsClient
    authentication_classes = TokenAuthentication
    serializer_class = UserUpdateSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            if user.is_anonymous:
                content = {'code': 1, 'detail': 'User is anonymous in user update'}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

            first_name = serializer.validated_data.get('first_name', '')
            last_name = serializer.validated_data.get('last_name', '')
            email = serializer.validated_data.get('email', '')
            temp = 0

            if first_name != '':
                user.first_name = first_name
                temp = 1

            if last_name != '':
                user.last_name = last_name
                temp = 1

            if email != '':
                user.email = email
                temp = 1

            if temp == 1:
                user.save()

            content = {'code': 0, 'first_name': user.first_name,
                       'last_name': user.last_name, 'email': user.email},
            return Response(content, status=status.HTTP_200_OK)

        else:
            content = {'code': 2, 'detail': 'error in user update api'}
            return Response(content, status=status.HTTP_200_OK)

############################
############################


class AddressApiView(APIView):
    # permission_classes = (IsClient,)
    serializer_class = AddressSerializer
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user
                if user.is_anonymous:
                    content = {'code': 1, 'detail': 'user is anonymous.'}
                    return Response(content, status=status.HTTP_200_OK)
                opt = self.kwargs.get('opt', '')
                if opt == 'delete':
                    id = serializer.data.get('id', '')
                    if id:
                        try:
                            add = Address.objects.get(id=id, user=user, status=1)
                            add.status = 0
                            add.save()
                            content = {'code': 0, 'detail': 'Address deleted.'}
                            return Response(content, status=status.HTTP_202_ACCEPTED)
                        except Address.DoesNotExist:
                            pass
                    content = {'code': 3, 'detail': 'Address Does not exist in deleting address.'}
                    return Response(content, status=status.HTTP_200_OK)
                elif opt == 'update':
                    try:
                        id = serializer.data.get('id', None)
                        lat = serializer.data.get('lat', None)
                        lng = serializer.data.get('lng', None)
                        if lat is not None and lng is not None:
                            lat = float(lat)
                            lng = float(lng)
                            location = {'type': 'Point', 'coordinates': [lng, lat]}
                        else:
                            location = None
                        address = serializer.data.get('address', '')
                        phone = serializer.data.get('phone', None)
                        name = serializer.data.get('name', None)
                        zipcode = serializer.data.get('zipcode', None)
                        add = Address.objects.get(id=id)
                        add = add.objects.update(user=user, phone=phone, zipcode=zipcode,
                                                 location=location, address=address, name=name)

                        content = {'id': add.id, 'name': add.name, 'lat': lat, 'lng': lng, 'address': add.addr,
                                   'user': user.id, 'phone': add.phone, 'zipcode': add.zip_code}
                        return Response(content, status=status.HTTP_202_ACCEPTED,
                                        headers={'Access-Control-Allow-Origin': '*'})
                    except Address.DoesNotExist:
                        content = {'code': 2, 'detail': 'address not exist in address update.'}
                        return Response(content, status=status.HTTP_200_OK)
                else:
                    try:
                        lat = serializer.data.get('lat', None)
                        lng = serializer.data.get('lng', None)
                        if lat is not None and lng is not None:
                            lat = float(lat)
                            lng = float(lng)
                            location = {'type': 'Point', 'coordinates': [lng, lat]}
                        else:
                            location = None
                        address = serializer.data.get('address', '')
                        phone = serializer.data.get('phone', None)
                        name = serializer.data.get('name', None)
                        zipcode = serializer.data.get('zipcode', None)
                        add = Address.objects.create(user=user, phone=phone, zipcode=zipcode,
                                                     location=location, address=address, name=name)

                        content = {'id': add.id, 'name': add.name, 'lat': lat, 'lng': lng, 'address': add.addr,
                                   'user': user.id, 'phone': add.phone, 'zipcode': add.zip_code}
                        return Response(content, status=status.HTTP_202_ACCEPTED,
                                        headers={'Access-Control-Allow-Origin': '*'})
                    except:
                        content = {'code': 2, 'detail': 'error occurred in address create.'}
                        return Response(content, status=status.HTTP_200_OK)
            except:
                content = {'code': 2, 'detail': 'error occurred in address api view.'}
                return Response(content, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_200_OK)


class AddressListAPIView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = AddressListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            user = self.request.user
            if user:
                addresses = Address.objects.filter(user=user)
                return addresses
            else:
                content = {'code': 0, 'detail': 'User Does not exist in List address.'}
                return Response(content, status=status.HTTP_200_OK)
        except:
            content = {'code': 1, 'detail': 'error in address list'}
            return Response(content, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers={'Access-Control-Allow-Origin': '*'})

############################
############################

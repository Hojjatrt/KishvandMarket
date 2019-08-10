import binascii
import os

import jdatetime
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from userapp.api.serializers import *
from userapp.models import *


def _generate_pass():
    return binascii.hexlify(os.urandom(20))


class Signup(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            phone = serializer.data['phone']
            check_sms_or_call = False
            must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)
            must_validate_sms = getattr(settings, "AUTH_SMS_VERIFICATION", True)

            try:
                user = get_user_model().objects.get(phone=phone)
                # if user.is_active:
                #     content = {'phone': phone,
                #                'code': 0,
                #                'status': 'no'
                #                }
                #     return Response(content, status=status.HTTP_200_OK)
                #     verified = True
                    # Delete old signup codes
                signup_sms_code = Sms.objects.filter(users=user).last()
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

            except Sms.DoesNotExist:
                pass

            except get_user_model().DoesNotExist:
                try:
                    user = get_user_model().objects.create_user(username=phone, phone=phone)
                    check_sms_or_call = True
                except:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Set user fields provided
            if not user.is_active:
                password = _generate_pass()
                user.set_password(password)

            user.save()
            if must_validate_sms:
                # Create and associate signup code
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '0.0.0.0')
                if x_forwarded_for:
                    ipaddr = x_forwarded_for.split(',')[0]
                else:
                    ipaddr = request.META.get('REMOTE_ADDR', '0.0.0.0')

                signup_sms_code = Sms.objects.create_sms_code(users=user, ipaddr=ipaddr)
                check_status = signup_sms_code.send_signup_sms()
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

        return Response(serializer.errors, status=status.HTTP_200_OK)


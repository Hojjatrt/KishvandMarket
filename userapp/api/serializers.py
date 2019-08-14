from django.core import validators
from rest_framework import serializers
from .validators import *
from django.utils.translation import ugettext_lazy as _


class SignupSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    phone = serializers.CharField(max_length=11, validators=[phoneValidator, ], error_messages={
        'unique': _("A user with that PhoneNumber already exists."), }, )

#########################
#########################


class VerifySerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    phone = serializers.CharField(max_length=11, validators=[phoneValidator, ])
    code = serializers.CharField(max_length=6)

#########################
#########################


class LoginSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    phone = serializers.CharField(max_length=11, validators=[phoneValidator, ])

#########################
#########################


class UserUpdateSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    first_name = serializers.CharField(max_length=30, validators=[validators.MinLengthValidator(limit_value=3), ],
                                       required=False)
    last_name = serializers.CharField(max_length=30, validators=[validators.MinLengthValidator(limit_value=3), ],
                                      required=False)
    email = serializers.EmailField(required=False)

#########################
#########################

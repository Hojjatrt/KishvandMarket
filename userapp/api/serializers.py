from django.core import validators
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .validators import *
from django.utils.translation import ugettext_lazy as _
from userapp.models import *

#########################
#########################


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


class AddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    phone = serializers.CharField(required=False, max_length=11, validators=[phoneValidator, ])
    name = serializers.CharField(max_length=30, required=False)
    zipcode = serializers.IntegerField(required=False)
    address = serializers.CharField(max_length=150, required=False)
    lat = serializers.DecimalField(max_digits=20, decimal_places=15, required=False)
    lng = serializers.DecimalField(max_digits=20, decimal_places=15, required=False)


class AddressListSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    lat = serializers.DecimalField(max_digits=20, decimal_places=15)
    lng = serializers.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        model = Address
        fields = ('id', 'user', 'phone', 'name', 'zipcode', 'addr', 'lat', 'lng')

    def to_representation(self, instance):
        geo = instance.point
        coordinates = geo['coordinates']
        lat = coordinates[1]
        lng = coordinates[0]

        return {
            "id": instance.id,
            "name": instance.name,
            "zipcode": instance.zipcode,
            "lat": lat,
            "lng": lng,
            "address": instance.addr,
            "user": instance.user.id,
            "phone": instance.phone,
        }

#########################
#########################


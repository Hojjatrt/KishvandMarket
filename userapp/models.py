from http.client import HTTPException
from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException

from KishvandMarket import settings
from django_jalali.db import models as jmodels

# Create your models here.


def _generate_sms_code():
    return randint(100000, 999999)

#########################
#########################


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (0, _('None')),
        (1, _('Normal User')),
        (2, _('Supervisor')),
        (3, _('Delivery')),
    )
    phone = models.CharField(_('Phone Number'), max_length=11, null=True, blank=True)
    usertype = models.PositiveSmallIntegerField(_('User Type'), choices=USER_TYPE_CHOICES, null=True,
                                                blank=True, default=0)

    def __str__(self):
        return self.username

#########################
#########################


class Address(models.Model):
    lat = models.CharField(_('Lat'), max_length=15)
    lng = models.CharField(_('Lng'), max_length=15)
    addr = models.TextField(_('Address'), max_length=300)
    phone = models.CharField(_('Phone number'), max_length=11)
    zip_code = models.CharField(_('ZipCode'), max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), null=True, blank=True,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.addr[:20] + '...'

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

#########################
#########################


class Massage(models.Model):
    text = models.TextField(_('Text'), max_length=300)
    name = models.CharField(_('name'), max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Massage")
        verbose_name_plural = _("Massages")

#########################
#########################


################################
################################


def send_multi_format_sms(template_prefix, data, target_phone):
    # subject_file = 'user/%s_subject.txt' % template_prefix
    # txt_file = 'user/%s.txt' % template_prefix
    # html_file = 'user/%s.html' % template_prefix

    try:
        api = KavenegarAPI('6538764672635A4C4C48346234417A75414D30476371635152372B5A585737344239346A645A564D3348773D')
        params = {
            'receptor': target_phone,
            'template': template_prefix,
            'token': data['code'],
            'type': data['type'],  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
        # if response['return']['status'] == 200:
        return response
    except APIException as e:
        print(e)
        return None
    except HTTPException as e:
        print(e)
        return None


class SmsCodeManager(models.Manager):
    def create_sms_code(self, user, ipaddr):
        code = _generate_sms_code()
        _sms_code = self.create(user=user, code=code, ipaddr=ipaddr)

        return _sms_code

    def set_user_is_verified(self, code, user):
        try:
            signup_code = Sms.objects.get(user=user, code=code)
            signup_code.user.is_active = True
            signup_code.user.save()
            signup_code.delete()
            return True
        except Sms.DoesNotExist:
            pass

        return False


class AbstractBaseSmsCode(models.Model):
    users = models.ManyToManyField(User, verbose_name=_('User'), null=True, blank=True)
    code = models.CharField(_('Code'), max_length=6, null=True, blank=True)
    created_at = jmodels.jDateTimeField(_('Created at'), auto_now_add=True, blank=True, null=True)

    class Meta:
        abstract = True

    def send_sms(self, prefix, type='sms'):
        data = {
            'username': self.users.username,
            'phone': self.users.phone,
            'code': self.code,
            'type': type,
        }
        return send_multi_format_sms(prefix, data, target_phone=self.users.phone)

    def __str__(self):
        return str(self.code)


class Sms(AbstractBaseSmsCode):
    massage = models.ForeignKey(Massage, verbose_name=_('Massage'), null=True, blank=True,
                                on_delete=models.DO_NOTHING)
    ipaddr = models.CharField(_('ip Address'), max_length=20, null=True, blank=True)
    # status = models.PositiveSmallIntegerField(_('Status'), null=True, blank=True)

    objects = SmsCodeManager()

    def send_signup_sms(self):
        prefix = 'verify'
        check = self.send_sms(prefix)
        print(check)
        if check is None:
            self.status = 0
            self.save()
            return 0
        else:
            self.status = 1
            self.save()
            return self.status

    def send_signup_call(self):
        prefix = 'verify'
        check = self.send_sms(prefix, type='call')
        print(check)
        if check is None:
            self.status = 0
            self.save()
            return 0
        else:
            self.status = check['status']
            self.save()
            return self.status

    def __str__(self):
        if self.code:
            return self.code
        else:
            return self.massage.name

    class Meta:
        verbose_name = _("Sms")
        verbose_name_plural = _("Smses")

#########################
#########################

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from KishvandMarket import settings

# Create your models here.

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
    text = models.CharField(_('Text'), max_length=300)
    name = models.CharField(_('name'), max_length=50)


#########################
#########################


class Sms(models.Model):
    code = models.CharField(_('Code'), max_length=6)
    user = models.ManyToManyField(User, verbose_name=_('User'), null=True, blank=True)
    massage = models.ForeignKey(Massage, verbose_name=_('Massage_id'), null=True, blank=True,
                                on_delete=models.CASCADE)
    date_time = models.DateField(_('Date_Time'))

#########################
#########################

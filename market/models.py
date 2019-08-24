from uuid import uuid4
import os, time
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from market.fields import *
import jsonfield
from sorl.thumbnail import ImageField
from userapp.models import Address
from django_jalali.db import models as jmodels
import jdatetime
# Create your models here.

#########################
#########################


@deconstructible
class PathAndRename(object):  # for path and rename a picture
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex[:8], ext)

        return os.path.join(self.path, filename)

#########################
#########################


class Category(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    parent = models.ForeignKey('self', verbose_name=_('Parent Category'), null=True, blank=True,
                               on_delete=models.CASCADE, related_name='children')
    thumbnail = models.ImageField(_('Thumbnail'),
                                  upload_to=PathAndRename('Cat/t/{}'.format(time.strftime("%Y/%m/%d"))),
                                  null=True, blank=True)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)
    param = jsonfield.JSONField(_('Parameters'), max_length=300)

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.__original_pic = self.thumbnail.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):

        if (self.thumbnail and self.pk is None) or self.__original_pic != self.thumbnail.name:
            self.thumbnail = resize(low_pic=self.thumbnail, high_pic=self.thumbnail, size=(300, 300))[0]

        super(Category, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_pic = self.thumbnail.name

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

#########################
#########################


class Baseinfo(models.Model):
    value = models.CharField(_('Value'), max_length=50)
    parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True,
                               on_delete=models.CASCADE)

    comment = models.TextField(_('Comment'), max_length=200, default='')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = _("Baseinfo")
        verbose_name_plural = _("Baseinfos")

#########################
#########################


class Tag(models.Model):
    title = models.CharField(_('Title'), max_length=25)

    def __str__(self):
        return '#' + self.title

#########################
#########################


class Product(models.Model):
    STATUS_CHOICES = (
        (True, _('Active')),
        (False, _('DeActive')),
    )

    UNIT_CHOICES = (
        (0, _('Number')),
        (1, _('Box')),
        (2, _('Liter')),
        (3, _('MiliLiter')),
        (4, _('Cc')),
        (5, _('KiloGram')),
        (6, _('Gram')),
        (7, _('MiliGram')),
    )

    name = models.CharField(_('Name'), max_length=50)
    status = models.BooleanField(_('Status'), blank=False, null=False, default=True,
                                 choices=STATUS_CHOICES, help_text=_("Status of Product"))
    unit = models.PositiveSmallIntegerField(_('Unit'), blank=False, null=False, default=0,
                                            choices=UNIT_CHOICES, help_text=_("Unit of Product"))
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'),
                                        related_name='Products')
    thumb = models.CharField(_('Thumbnail'), max_length=20, null=True, blank=True, editable=False)
    order = models.PositiveIntegerField(_('Order'), default=0)
    tags = models.ManyToManyField(Tag, verbose_name=_('Tags'))

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None, *args, **kwargs):
    #     imgs = Image.objects.filter(prod=self.id, main=True).last()
    #     if imgs is not None:
    #         self.thumb = imgs.image.name
    #     super(Product, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.name

#########################
#########################


class ProductSpecie(models.Model):
    text = models.TextField(_('Text'), max_length=200)
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20] + "..."

#########################
#########################


class ProductParameter(models.Model):
    parameters = jsonfield.JSONField(_('Parameters'), max_length=300)
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.parameters[:20] + "..."

#########################
#########################


class Stock(models.Model):
    price = models.BigIntegerField(_('Price'), help_text=_('Sell in Toman'), default=0)
    discount_ratio = models.PositiveSmallIntegerField(_('Discount Ratio'), help_text=_('Discount percent %'),
                                                      default=0)
    qnt = models.PositiveIntegerField(_('Quantity'), default=0)
    product = models.ForeignKey(Product, verbose_name=_('Quantity'), on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.price)

#########################
#########################


class Image(models.Model):
    image = ImageField(_('Image'), upload_to=PathAndRename('prod/'),
                       null=True, blank=True)
    prod = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE, null=True)
    main = models.BooleanField(_('Main Image'), default=False)

    def __init__(self, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        self.__original_pic = self.image.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):

        if (self.image and self.pk is None) or self.__original_pic != self.image.name:
            self.image = resize(low_pic=self.image, high_pic=self.image, size=(700, 700))[0]

        super(Image, self).save(force_insert, force_update, *args, **kwargs)
        if self.main:
            self.prod.thumb = self.image.name
            self.prod.save(force_update=True)

        self.__original_pic = self.image.name

    def __str__(self):
        return self.image.name


#########################
#########################


class Discount(models.Model):
    code = models.CharField(_('Code'), max_length=20)
    percent = models.PositiveSmallIntegerField(_('Percent'), default=0)
    name = models.CharField(_('Name'), max_length=30)

    def __str__(self):
        return self.code


#########################
#########################


class Time(models.Model):
    time = models.CharField(_('Time'), max_length=15)

    @property
    def strparse(self):
        start = jdatetime.datetime.strptime(self.time.split(' - ')[0], '%H:%M').time()
        return start

    def __str__(self):
        return self.time

#########################
#########################


class Cart(models.Model):
    STATUS_CHOICES = (
        (0, _('Doing')),
        (1, _('Unpaid')),
        (2, _('Paid')),
        (3, _('Sending')),
        (4, _('Done')),
    )
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Customer'),
                                 on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, verbose_name=_('Product'))
    discount = models.ForeignKey(Discount, verbose_name=_('Discount'), on_delete=models.DO_NOTHING,
                                 null=True, blank=True)
    address = models.ForeignKey(Address, verbose_name=_('Address'), on_delete=models.DO_NOTHING)
    time = models.ForeignKey(Time, verbose_name=_('Time'), on_delete=models.DO_NOTHING)
    date = jmodels.jDateField(_('Date'))
    created_at = jmodels.jDateTimeField(_('Created at'), auto_now_add=True)
    status = models.PositiveSmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=0)
    amount = models.PositiveIntegerField(_('Amount'), default=0)

    def __str__(self):
        return str(self.customer) + str(self.amount)

#########################
#########################


class ExcludeDate(models.Model):
    DAY_CHOICES = (
        (0, _('Saturday')),
        (1, _('Sunday')),
        (2, _('Monday')),
        (3, _('Tuesday')),
        (4, _('Wednesday')),
        (5, _('Thursday')),
        (6, _('Friday')),
    )
    date = jmodels.jDateField(_('Date'), null=True, blank=True)
    times = models.ManyToManyField(Time, verbose_name=_('Times'))
    day = models.PositiveSmallIntegerField(_('Day'), choices=DAY_CHOICES, null=True, blank=True)

    def __str__(self):
        if self.date:
            return str(self.date)
        else:
            return str(self.DAY_CHOICES[self.day][1])

    class Meta:
        verbose_name = _("ExcludeDate")
        verbose_name_plural = _("ExcludeDates")


#########################
#########################

class Slide(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    image = ImageField(_('Image'), upload_to=PathAndRename('slides/'))
    link = models.URLField(
        _("Link"),
        max_length=128,
        blank=True
    )

    def __init__(self, *args, **kwargs):
        super(Slide, self).__init__(*args, **kwargs)
        self.__original_pic = self.image.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):

        if (self.image and self.pk is None) or self.__original_pic != self.image.name:
            self.image = resize(low_pic=self.image, high_pic=self.image, size=(300, 300))[0]

        super(Slide, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_pic = self.image.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")

#########################
#########################

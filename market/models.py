from uuid import uuid4
import os, time

from django.core.validators import MinValueValidator, MaxValueValidator
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


class Parameters(models.Model):
    key = models.CharField(_('Key'), max_length=30)

    def __str__(self):
        return str(self.key)

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameters")

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
    param = models.ManyToManyField(Parameters, verbose_name=_('Parameters'))

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
    parameters = models.ManyToManyField(Parameters, through='ParameterValue', verbose_name=_('Parameters'))

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None, *args, **kwargs):
    #     imgs = Image.objects.filter(prod=self.id, main=True).last()
    #     if imgs is not None:
    #         self.thumb = imgs.image.name
    #     super(Product, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.name


class ParameterValue(models.Model):
    parameter = models.ForeignKey(Parameters, verbose_name=_('Parameter'), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE)
    value = models.CharField(_('Value'), max_length=30, null=True, blank=True)

    def __str__(self):
        return str(self.parameter.key) + ' -> ' + str(self.value)

    class Meta:
        verbose_name = _("Parameter Value")
        verbose_name_plural = _("Parameter Values")

#########################
#########################


class ProductSpecie(models.Model):
    text = models.TextField(_('Text'), max_length=200)
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20] + "..."

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
    PAYMENT_CHOICES = (
        (0, _('Cash')),
        (1, _('Card')),
        (2, _('Online')),
    )
    code = models.CharField(_('Tracking Code'), max_length=15, unique=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Customer'),
                                 on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, verbose_name=_('Products'), through='CartProduct')
    discount = models.ForeignKey(Discount, verbose_name=_('Discount'), on_delete=models.DO_NOTHING,
                                 null=True, blank=True)
    address = models.ForeignKey(Address, verbose_name=_('Address'), on_delete=models.DO_NOTHING)
    time = models.ForeignKey(Time, verbose_name=_('Time'), on_delete=models.DO_NOTHING)
    date = jmodels.jDateField(_('Date'))
    created_at = jmodels.jDateTimeField(_('Created at'), auto_now_add=True)
    status = models.PositiveSmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=0)
    amount = models.PositiveIntegerField(_('Amount'), default=0)
    pay_method = models.PositiveSmallIntegerField(_('Payment Method'), default=0, choices=PAYMENT_CHOICES)
    # TODO after we write payment model uncomment this
    # payment = models.ForeignKey(Payment, verbose_name=_('Payment'), on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            # last_id = Cart.objects.all().aggregate(largest=models.Max('code'))['largest']
            last_card = Cart.objects.all().last()
            if last_card is not None:
                print(last_card, last_card.code)
            print(last_card)
            # aggregate can return None! Check it first.
            self.coding(last_card)
        super(Cart, self).save(*args, **kwargs)

    def coding(self, last):
        MONTH_CHOICES = (
            (1, 'A'),
            (2, 'B'),
            (3, 'C'),
            (4, 'D'),
            (5, 'E'),
            (6, 'G'),
            (7, 'H'),
            (8, 'I'),
            (9, 'J'),
            (10, 'K'),
            (11, 'L'),
            (12, 'M'),
        )
        date = jdatetime.datetime.now().date()
        year = str(date.year)[2:]
        month = MONTH_CHOICES[date.month - 1][1]
        if last is None:
            self.code = year + month + '-' + str(100001)
            return
        last_code = last.code.split('-')
        if year + month == last_code[0]:
            self.code = year + month + '-' + str(int(last_code[1]) + 1)
        else:
            self.code = year + month + '-' + str(100001)
        return

    def __str__(self):
        return str(self.code) + ' : ' + str(self.amount)


class CartProduct(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name=_('Cart'), on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(_('Number of Products'))

    def __str__(self):
        return str(self.product) + ' with ' + str(self.number) + ' no.'

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
            self.image = resize(low_pic=self.image, high_pic=self.image, size=(1000, 800))[0]

        super(Slide, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_pic = self.image.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")

#########################
#########################
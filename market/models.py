from uuid import uuid4
import os, time
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from market.fields import *
import jsonfield
from sorl.thumbnail import ImageField

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
    param = jsonfield.JSONField(_('Parameters'), max_length=300, null=True, default=[])

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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        imgs = Image.objects.filter(prod=self.id, main=True).last()
        if imgs is not None:
            self.thumb = imgs.image.name
        super(Product, self).save(force_insert, force_update, *args, **kwargs)

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
        self.__original_pic = self.image.name

    def __str__(self):
        return self.image.name

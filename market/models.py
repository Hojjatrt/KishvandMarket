from uuid import uuid4
import os, time
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

# Create your models here.


#########################
#########################

@deconstructible
class PathAndRename(object):  # for path and rename a picture
    def __init__(self, sub_path, base):
        self.path = sub_path
        self.base = base

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}-pk{}-{}.{}'.format(self.base, instance.pk, uuid4().hex[:5], ext)

        return os.path.join(self.path, filename)

#########################
#########################

class MainCategory(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    image = models.ImageField(_('Image'),
                                upload_to=PathAndRename('Categories/{}'.format(time.strftime("%Y/%m/%d")), 'Category'),
                                null=True, blank=True)
    thumbnail = models.ImageField(_('Thumbnail'),
                                  upload_to=PathAndRename('Categories/thumbnails/{}'.format(time.strftime("%Y/%m/%d")),
                                                          'Category'),
                                  null=True, blank=True, editable=False)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("MainCategory")
        verbose_name_plural = _("MainCategories")

#########################
#########################

class SubCategory(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    parent = models.ForeignKey(MainCategory, on_delete=models.DO_NOTHING, verbose_name=_('Parent'))
    order = models.PositiveSmallIntegerField(_('Order'), default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("SubCategory")
        verbose_name_plural = _("SubCategories")

#########################
#########################


class Product(models.Model):
    __original_status = None
    __original_pic = None

    STATUS_CHOICES = (
        (1, _('Active')),
        (0, _('DeActive')),
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
    status = models.PositiveSmallIntegerField(_('Status'), blank=False, null=False, default=1,
                                       choices=STATUS_CHOICES, help_text=_("Status of Product"))
    unit = models.PositiveSmallIntegerField(_('Unit'), blank=False, null=False, default=0,
                                     choices=UNIT_CHOICES, help_text=_("Unit of Product"))
    price = models.BigIntegerField(_('Price'), help_text=_('Sell in Toman'))
    discount_ratio = models.PositiveSmallIntegerField(_('Discount Ratio'), help_text=_('Discount percent'))
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name=_('Category'),
                                 related_name='Products')
    image = models.ImageField(_('Image'),
                                upload_to=PathAndRename('products/{}'.format(time.strftime("%Y/%m/%d")), 'Product'),
                                null=True, blank=True)
    thumbnail = models.ImageField(_('Thumbnail'),
                                  upload_to=PathAndRename('products/thumbnails/{}'.format(time.strftime("%Y/%m/%d")),
                                                          'Product'),
                                  null=True, blank=True, editable=False)
    order = models.PositiveIntegerField(_('Order'), default=0)
    capacity = models.PositiveIntegerField(_('Capacity'), default=0)
    tags = models.ManyToManyField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

#########################
#########################

class Tag(models.Model):
    title = models.CharField(_('Title'), max_length=25)

    def __str__(self):
        return '#' + self.title

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

#########################
#########################


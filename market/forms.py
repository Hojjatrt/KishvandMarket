from dal import autocomplete
from django import forms
from django.contrib.admin import widgets
from .models import *
from django.utils.translation import ugettext_lazy as _
from django_jalali.admin.widgets import AdminjDateWidget


class ParameterValueAdminForm(forms.ModelForm):
    class Meta:
        model = ParameterValue
        fields = '__all__'
        widgets = {
            'parameter': autocomplete.ModelSelect2(url='parameter-autocomplete')
        }


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'categories': autocomplete.ModelSelect2Multiple(url='subcategory-autocomplete'),
            'tags': autocomplete.ModelSelect2Multiple(url='tag-autocomplete')
        }

#######################
#######################


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        # exclude = ('param',)
        fields = '__all__'
        widgets = {
            'param': autocomplete.ModelSelect2Multiple(url='parameter-autocomplete')
        }

#######################
#######################


class CartAdminForm(forms.ModelForm):

    class Meta:
        model = Cart
        fields = '__all__'
        widgets = {
            'date': AdminjDateWidget
        }

#######################
#######################


class TimeAdminForm(forms.ModelForm):
    start = forms.TimeField(required=True, widget=widgets.AdminTimeWidget(format="%H:%M"))
    end = forms.TimeField(required=True, widget=widgets.AdminTimeWidget(format="%H:%M"))
    time = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(TimeAdminForm, self).clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if end <= start:
            msg = _('End time should not occur before start time.')
            self._errors['end'] = self.error_class([msg])
            del cleaned_data['end']
        elif start and end:
            cleaned_data['time'] = start.strftime("%H:%M") + ' - ' + end.strftime("%H:%M")
        return cleaned_data

    class Meta:
        model = Time
        fields = '__all__'

#######################
#######################


class CartProductAdminForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = '__all__'
        widgets = {
            'product': autocomplete.ModelSelect2(url='product-autocomplete'),
        }

#######################
#######################

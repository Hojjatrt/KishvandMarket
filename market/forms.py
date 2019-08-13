from dal import autocomplete
from django import forms
from django.contrib.admin import widgets
from .models import *
from django.utils.translation import ugettext_lazy as _
from django_jalali.admin.widgets import AdminjDateWidget


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'categories': autocomplete.ModelSelect2Multiple(url='subcategory-autocomplete'),
            'tags': autocomplete.ModelSelect2Multiple(url='tag-autocomplete')
        }


class CategoryAdminForm(forms.ModelForm):
    para = forms.CharField(max_length=50, required=True)
    value = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Category
        exclude = ('param',)

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

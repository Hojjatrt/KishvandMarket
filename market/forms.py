from dal import autocomplete
from django import forms
from .models import *


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

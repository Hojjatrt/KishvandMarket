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

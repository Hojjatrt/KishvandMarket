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

#######################
#######################


class TimeAdminForm(forms.ModelForm):
    start = forms.TimeField(required=True)
    end = forms.TimeField(required=True)
    time = forms.CharField(required=False)

    def save(self, commit=True):
        f = super(TimeAdminForm, self).save(commit=False)
        print(f)
        if commit:
            print(f)
            self.instance.time = str(self.cleaned_data['start']) + ' - ' + str(self.cleaned_data['end'])
            f.save()
        return f

    class Meta:
        model = Time
        fields = '__all__'
        widgets = {
            'start': forms.TimeInput,
            'end': forms.TimeInput,
        }

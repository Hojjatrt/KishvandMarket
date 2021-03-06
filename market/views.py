from django.shortcuts import render
from dal import autocomplete
from .models import *

# Create your views here.

##################
##################


class SubCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Category.objects.none()

        qs = Category.objects.filter(parent__isnull=False)

        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs

##################
##################


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs

##################
##################


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Product.objects.none()

        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

##################
##################


class ParameterAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Parameters.objects.none()

        qs = Parameters.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

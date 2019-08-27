from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path(r'^api/', include('market.api.urls'))
    path('subcategory-autocomplete/',
         SubCategoryAutocomplete.as_view(),
         name='subcategory-autocomplete',
         ),
    path('tag-autocomplete/',
         TagAutocomplete.as_view(),
         name='tag-autocomplete',
         ),
    path('product-autocomplete/',
         ProductAutocomplete.as_view(),
         name='product-autocomplete',
         ),
    path('parameter-autocomplete/',
         ParameterAutocomplete.as_view(),
         name='parameter-autocomplete',
         ),
]

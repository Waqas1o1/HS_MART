from django.urls import path 
from . import views
urlpatterns = [
    path('',views.index),
    path('Item/<int:code>',views.ItemScanner),
    path('autocomplete/',views.autocompleteModel),
    path('Barcode/<int:barcode>',views.AddItemBarcode),
    path('Productname/<str:pdtname>',views.AddItemByPdtName),
    path('autosuggest/',views.autosuggest,name="autosuggest"),
    path('GenrateBill_Genrated/',views.GenrateBill_Genrated),
    path('Findkhaata/',views.Find_Khaata,name='Findkhaata'),
]

from django.urls import path
from . import views
from Store_App import views as v
urlpatterns = [
    path('',views.Bill_Analysis,name='BillAnalysis'),
    path('GetGraph/<str:year>',views.Get_Graph),
    path('ProfitGraph/',views.Graph_Analysis,name='GraphAnalysis'),
    path('FindKhaata/',v.Find_Khaata,name='Findkhaata')
]

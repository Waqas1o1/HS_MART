from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',RedirectView.as_view(url='Home/')),
    path('Home/',include('Store_App.urls')),
    path('Analysis/',include('DataAnalysis.urls')),
]+ static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)

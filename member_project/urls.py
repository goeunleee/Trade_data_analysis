"""register_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
import registerapp.views
import cloudapp.views
import jobapp.views
import Open_APP.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Open_APP.views.main, name='main'),
    path('register/', include('registerapp.urls')),
    path('jobapp/', include('jobapp.urls')),
    path('Open_APP/',include('Open_APP.urls')),
    path('upload_cloud/',cloudapp.views.upload_cloud,name="upload_cloud"),
    path('upload_cloud/<int:idx>/delete',cloudapp.views.delete,name='delete'),
    # path('upload_cloud/dataTransmit/', cloudapp.views.dataTransmit, name='dataTransmit')
    url(r'^upload_cloud/dataTransmit/$', cloudapp.views.dataTransmit, name='dataTransmit'),
]
urlpatterns += \
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

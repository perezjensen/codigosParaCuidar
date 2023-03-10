"""codigos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from perfilMascotas import urls
from adminCodigos import urls

from django.conf import settings # se utiliza para la carga de imagen 
from django.conf.urls.static import static # se utiliza para la carga de imagen

from django.contrib import messages




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('perfilMascotas.urls')),
    path('', include('adminCodigos.urls')),
    path('', include('web.urls')),
    
]


#añadimos a las url las url para buscar las imagenes 
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT )


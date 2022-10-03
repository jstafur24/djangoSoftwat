"""SOFTWAT URL Configuration

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .import views
from django.urls import include
from GestionProductos.views import ProductListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.paginaprincipal, name='index'),
    path('clienteinicio/', views.register, name='iniciocliente'),
    path('mision/', views.Mision, name='mision'),
    path('catpinturas/', ProductListView.as_view(), name='catpinturas'), #indicamos que vamos a usar la clase como una vista
    path('catrollos/', views.CatRollos, name='catrollos'),
    path('aplicacion/', views.Aplicacion, name='aplicacion'),
    path('domicilio/', views.Domicilio, name='domicilio'),
    path('login/', views.login_view, name='login'),
    path('usuarios/logout/', views.logout_view, name='logout'),
    path('PQRS/', views.PQRS, name='PQRS'),
    path('carrito/', include('carts.urls')),
    path('Estado/',views.Estado, name='estado'),
    path('Actualizar/',views.Actualizar, name='actualizar'),
    path('productos/', include('GestionProductos.urls')),
    path('orden/', include('orders.urls')),
    path('direcciones/', include('shipping_addresses.urls')),


    #img
    path('admin/', admin.site.urls, name='admin'),


]

#img
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
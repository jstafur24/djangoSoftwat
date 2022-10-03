from unicodedata import name
from django.urls import path

from .import views

# Aplicacion en la que se implementa
app_name = 'orders'

# url de la pagina order
urlpatterns = [
    path('', views.order, name='order'),
    path('direccion', views.address, name='address'),
    path('seleccionar/direccion', views.select_address, name='select_address'),
    path('establecer/direccion/<int:pk>', views.check_address, name='check_address'),
    path('confirmacion', views.confirm, name='confirm'),
    path('cancelar', views.cancel, name='cancel'),
    path('completar', views.complete, name='complete')
]
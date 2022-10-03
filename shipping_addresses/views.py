from ast import Delete, arg
from email import message
from http.client import HTTPResponse
from msilib.schema import ListView
from pyexpat.errors import messages
from django.shortcuts import render
from django.views.generic import ListView
from orders.utils import get_or_create_order

import shipping_addresses
from .models import ShippingAddress
from .forms import ShippingAddressForm
#-----------------------------------------
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required #esto hace que se restringa el acceso a usuarios no autenticados
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order
from django.http import HttpResponseRedirect


class ShippingAddressListView(LoginRequiredMixin, ListView):
    login_url = 'login' #reedirigir a login
    model = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')
# obtenemos todas las direcciones del usuari y las registramos con el atributo default

#para editar direcciones
class ShippingAddressUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = ShippingAddress #indicamos un modelo
    form_class = ShippingAddressForm # indicamos un formulario 
    template_name = 'shipping_addresses/update.html' #y indicamos un templeate
    

    def get_succes_url(self):
        return reverse('shipping_addresses:shipping_addresses')

    #PARA HACKERS QUE QUIERAN CAMBIAR O SABER DIRECCIONES DE USUARIOS
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)


class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login' #permite conocer a donde redirigir si no se esta lgoeado
    model = ShippingAddress
    template_name = 'shipping_addresses/delete.html'
    success_url = reverse_lazy('shipping_addresses:shipping_addresses')

def dispatch(self, request, *args, **kwargs):
    if self.get_object().default:
        return redirect('shipping_addresses:shipping_addresses')

    if request.user.id != self.get_object().user_id:
        return redirect(' carts:cart ')

    return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)
    

@login_required(login_url='login') #para dar una direccion al usuario anonimo
def create(request):

    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False) #para que se guarde en la base de datos
        shipping_address.user = request.user #tiene que haber un usuario 
        shipping_address.default = ShippingAddress.objects.filter(user=request.user).exists()
        
        #Si existen direcciones de ese usario en entonces default es falso
        #si no existen direcciones es verdadero

        shipping_address.save()  #se guarda la informacion

        if request.GET.get('next'):
            if request.GET['next'] == reverse('orders:address'):
                cart = get_or_create_cart(request)
                order = get_or_create_order(cart, request)

                order.update_shipping_address(shipping_address)

                return HttpResponseRedirect(request.GET['next'])


        messages.success(request, 'Direccion creada exitosamente') #Mensaje pero no sale
        return redirect('shipping_addresses:shipping_addresses') # y cuando se guarde la informacion nos rediriga a mis direcciones


    return render(request, 'shipping_addresses/create.html', {
        'form': form


    })

def default(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    if request.user.has_shipping_address():
        request.user.shipping_address.update_default()

#antes de acctualizar se debe tener la antigua direccion principal y colocar default como falso
    request.user.shipping_address.update_default()
    shipping_address.update_default(True)

    return redirect('shipping_addresses:shipping_addresses')


from django.shortcuts import redirect
from django.shortcuts import render
from GestionProductos.models import Product
from .utils import get_or_create_cart

from .models import CartProducts

def cart(request):
    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', {
        'cart': cart
    })

def add(request):
    cart = get_or_create_cart(request)
    product = Product.objects.get(pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1)) 
    
    # cart.products.add(product, through_defaults ={
    #     'quantity' : quantity
    # } )
    cart_product = CartProducts.objects.create_or_update_quantity(cart=cart, product=product, quantity=quantity)

    return render(request, 'carts/add.html', {
        'product': product
    })

def remove(request):
    cart = get_or_create_cart(request)
    product = Product.objects.get(pk=request.POST.get('product_id')) 

    cart.products.remove(product)

    return redirect('carts:cart')
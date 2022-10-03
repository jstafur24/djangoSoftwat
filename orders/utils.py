from .models import Order

def get_or_create_order(cart, request):
    order = Order.objects.filter(cart=cart).first()  #si un objeto no sirve levanta una exepcion

    if order is None and request.user.is_authenticated:  # si la orden no existe entonces :
        order = Order.objects.create(cart=cart, user=request.user) #el usuario debe estar autenticado
    
    if order:  # si la orden existe entonces de actualiza la sesion
        request.session['order_id'] = order.order_id
    return order


def destroy_order(request):
    request.session['order_id'] = None
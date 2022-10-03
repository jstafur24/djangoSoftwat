from tkinter import CASCADE
import uuid

from shipping_addresses.models import ShippingAddress
from enum import Enum
from ftplib import MAXLINE
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from carts.models import Cart
from django.db.models.signals import pre_save

import shipping_addresses
from shipping_addresses.models import ShippingAddress

class OrderStatus(Enum) : #Estado de la orden
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

#lista de tuplas
choices = [(tag, tag.value) for tag in OrderStatus ]


class Order(models.Model):
    order_id = models.CharField(max_length=100, null=False, blank=False, unique=True) # unique es que sea un modelo unico
    user = models.ForeignKey(User,on_delete=models.CASCADE) #uno a muchos
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE ) #uno a muchos
    status = models.CharField(max_length=50, choices=choices, default = OrderStatus.CREATED) #choiches=opciones

    shipping_total = models.DecimalField(default=5, max_digits=8, decimal_places=2) #Valor de envio
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)  #carrito de compras+total envio
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(ShippingAddress, null=True, blank=True, on_delete=models.CASCADE)



    def __str__(self):
        return self.order_id                         #retornamos order_id
    
    def get_or_set_shipping_address(self): #si la orden tiene una direccion de envio entonces se obtiene
        if self.shipping_address:
            return self.shipping_address

        shipping_address = self.shipping_address  #en caso contrario intentar buscar direccion principal
        if shipping_address:
            self.update_shipping_address(shipping_address)
        return shipping_address

    def update_shipping_address(self, shipping_address):
        self.shipping_address = shipping_address
        self.save()


    def cancel(self):       # para destruir la orden
        self.status =OrderStatus.CANCELED
        self.save()

    
    def complete(self):
        self.status = OrderStatus.COMPLETED
        self.save()





    def update_total(self):
        self.total = self.get_total()
        self.save()
        
    def get_total(self):
        return self.cart.total + self.shipping_total

def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
         instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total

pre_save.connect(set_order_id, sender=Order) #antes de almacenar
# pre_save.connect(set_total, sender=Order) #antes que un objeto order se almacene pone total
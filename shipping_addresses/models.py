from email.policy import default
from pyexpat import model
from re import T
from django.db import models
from django.contrib.auth.models import User


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    reference = models.CharField(max_length=300)
    codpost = models.CharField(max_length=10)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.codpost

    def update_dafault(self, default=False):
        self.default = default
        self.save()

    @property #Para convertir un metodo en una propiedad usar
    def address(self): #propiedad
        return '{} - {} - {}' .format(self.city, self.state, self.country) 


    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    def has_shipping_address(self):
        return self.shipping_address is not None
from msilib.schema import ListView
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product
from django.db.models import Q
# Create your views here.

class ProductListView(ListView):
    template_name = 'PINTURAS.HTML' #template donde se reflejara la lista de productos
    queryset = Product.objects.all().order_by('-id') # consulta para obtener el listado de objetos

    # este metodo se encarga de pasar el contexto de la clase a el template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['message'] = 'Listado De Productos'

        print(context)
        return context
# la clase DetailView se encarga de obtener un objeto, un regustro de nuestra base de datos a partir de un identificador 'id' llave primaria 'pk'
class ProductDetailView(DetailView):

    model = Product
    template_name = 'products/product.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print(context)
        return context

class PrductSearchListView(ListView):
    template_name = 'products/search.html'

    def get_queryset(self):
        # se definen los filtros con los cuales se pueden buscar productos
        filters = Q(name__icontains=self.query())  | Q(category__name__icontains=self.query())
        return Product.objects.filter(filters)

    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['query'] = self.query()
        context['count'] = context['product_list']. count()

        print(context)
        return context
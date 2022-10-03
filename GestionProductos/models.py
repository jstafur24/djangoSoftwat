import uuid
from venv import create

from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

class marca(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripcion')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        db_table = 'Marca'
        ordering = ['id']

class category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripcion')
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'Categoria'
        ordering = ['id']

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripcion')
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0.0, verbose_name='Precio')
    image = models.ImageField(upload_to='media', null=False, blank=False)
    category = models.ManyToManyField(category)
    marca = models.ForeignKey(marca, on_delete=models.CASCADE)
    slug = models.SlugField(null=False, blank=True, unique=True)
    #created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
         self.slug = slugify(self.name)
         super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

def set_slug(sender, instance, *args, **kwargs):#callback
    if instance.name and not instance.slug:
        slug = slugify(instance.name)

        while Product.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.name, str(uuid.uuid4())[:8] ) #el metodo uuid nos retorna un objeto
            )

        instance.slug = slug

pre_save.connect(set_slug, sender=Product)

class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        db_table = 'Producto'
        ordering = ['id'] #ordenar los registros que se organizan por su id 



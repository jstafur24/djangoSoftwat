# Generated by Django 4.1.1 on 2022-09-26 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionProductos', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]

from django.contrib import admin

from .models import (Categoria, Producto, ProductoEnCarrito, ProductoSubcategoria, Subcategoria)

admin.site.register(Categoria)
admin.site.register(ProductoEnCarrito)
admin.site.register(ProductoSubcategoria)
admin.site.register(Producto)
admin.site.register(Subcategoria)

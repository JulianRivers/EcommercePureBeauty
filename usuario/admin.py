from django.contrib import admin

from .models import (Carrito,Ciudad,Departamento,Pais,UserProfile)

admin.site.register(Carrito)
admin.site.register(Ciudad)
admin.site.register(Departamento)
admin.site.register(Pais)
admin.site.register(UserProfile)

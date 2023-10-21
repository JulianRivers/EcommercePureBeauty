from django.contrib import admin

from .models import (UserProfile, Departamento, Evento, TipoViatico, Viatico, AsistenciaEvento)

admin.site.register(UserProfile)
admin.site.register(Departamento)
admin.site.register(Evento)
admin.site.register(TipoViatico)
admin.site.register(AsistenciaEvento)
admin.site.register(Viatico)


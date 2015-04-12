from django.contrib import admin
from models import *


class Admin(admin.ModelAdmin):
    """docstring for ClientesAdmin"""
    pass

class TiendaAdmin(admin.ModelAdmin):
    """docstring for ClientesAdmin"""
    pass

admin.site.register(Administrador,Admin)
admin.site.register(Tienda,TiendaAdmin)
admin.site.register(Modelos)
admin.site.register(Productos)
admin.site.register(Stock)
admin.site.register(Extras)
admin.site.register(Pedidos)
admin.site.register(Unidades)
admin.site.register(Galeria)
admin.site.register(Formapago)
admin.site.register(TiendaFormapago)
#sadmin.site.register(Site)

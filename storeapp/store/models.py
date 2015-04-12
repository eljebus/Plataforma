# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.contrib.sites.models import Site
from autoslug import AutoSlugField

class Administrador(models.Model):
    idadministrador = models.AutoField(primary_key=True, db_column='idAdministrador') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre' ) # Field name made lowercase.
    login = models.CharField(max_length=135, db_column='Login' ) # Field name made lowercase.
    password = models.CharField(max_length=135, db_column='Pass' ) # Field name made lowercase. Field renamed because it was a Python reserved word.
    cliente = models.CharField(max_length=135, db_column='Cliente' ) # Field name made lowercase.
    activo = models.IntegerField(null=True, db_column='Activo' ) # Field name made lowercase.
    class Meta:
        db_table = u'Administrador'

class Tienda(models.Model):
    idtienda = models.AutoField(primary_key=True, db_column='idTienda') # Field name made lowercase.
    nombre = models.CharField(max_length=450, db_column='Nombre') # Field name made lowercase.
    rfc = models.CharField(max_length=45, db_column='RFC') # Field name made lowercase.
    logo = models.CharField(max_length=450, db_column='Logo') # Field name made lowercase.
    ubicacion = models.CharField(max_length=135, db_column='Ubicacion' ) # Field name made lowercase.
    direccion = models.CharField(max_length=135, db_column='Direccion' ) # Field name made lowercase.
    mail = models.CharField(max_length=135, db_column='Mail') # Field name made lowercase.

    telefono=models.CharField(max_length=27, db_column='Telefono') # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion')
    activo = models.IntegerField(null=True, db_column='Activo') # Field name made lowercase.
    administrador = models.ForeignKey(Administrador, db_column='Administrador') # Field name made lowercase.

    site = models.ForeignKey(Site)
    class Meta:
        db_table = u'Tienda'


class Anuncios(models.Model):
    idanuncios = models.AutoField(primary_key=True, db_column='idAnuncios') # Field name made lowercase.
    nombre=models.CharField(max_length=435, db_column='Nombre') # 

    fecha = models.DateTimeField(db_column='Fecha') # Field name made lowercase.
    imagen = models.CharField(max_length=435, db_column='Imagen') # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion') # Field name made lowercase.

    tipo = models.CharField(max_length=3,db_column='Tipo')

    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    tienda = models.ForeignKey(Tienda, db_column='Tienda') # Field name made lowercase.
    class Meta:
        db_table = u'Anuncios'


class Stock(models.Model):
    idstock = models.AutoField(primary_key=True, db_column='idStock') # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha') # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion') # Field name made lowercase.
    tienda = models.ForeignKey(Tienda, db_column='Tienda') # Field name made lowercase.
    class Meta:
        db_table = u'Stock'

class Tipocliente(models.Model):
    idtipocliente = models.AutoField(primary_key=True, db_column='idTipoCliente') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre' ) # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion' ) # Field name made lowercase.
    prioridad = models.CharField(max_length=3, db_column='Prioridad' ) # Field name made lowercase.
    stock_idstock = models.ForeignKey(Stock, db_column='Stock_idStock') # Field name made lowercase.
    class Meta:
        db_table = u'TipoCliente'

class Clientes(models.Model):
    idclientes = models.AutoField(primary_key=True, db_column='idClientes') # Field name made lowercase.
    nombre = models.CharField(max_length=450, db_column='Nombre') # Field name made lowercase.
    domicilio = models.CharField(max_length=600, db_column='Domicilio') # Field name made lowercase.
    cp = models.CharField(max_length=60, db_column='CP') # Field name made lowercase.
    estado = models.CharField(max_length=60, db_column='Estado') # Field name made lowercase.
    mail = models.CharField(max_length=300, db_column='Mail') # Field name made lowercase.
    tel = models.CharField(max_length=300, db_column='Tel')
    password=models.CharField(max_length=300, db_column='Pass')
    tipocliente = models.ForeignKey(Tipocliente, db_column='TipoCliente') # Field name made lowercase.
    tienda = models.ForeignKey(Tienda, db_column='Tienda')
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.

    class Meta:
        db_table = u'Clientes'

class Unidades(models.Model):
    nombre = models.CharField(max_length=150, primary_key=True, db_column='Nombre') # Field name made lowercase.
    prefijo = models.CharField(max_length=135)
    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = u'Unidades'

class Formapago(models.Model):
    nombre = models.CharField(max_length=45,primary_key=True, db_column='Nombre') # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion' ) # Field name made lowercase.
    logo = models.CharField(max_length=135, db_column='Logo' ) # Field name made lowercase.
    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = u'FormaPago'

class TiendaFormapago(models.Model):
    tienda = models.ForeignKey(Tienda, db_column='Tienda', primary_key=True) # Field name made lowercase.
    #formapago = models.ForeignKey(Formapago, db_column='FormaPago', primary_key=True) # Field name made lowercase.
    formapago = models.ForeignKey(Formapago, db_column='FormaPago')
    llaveprivada=models.CharField(max_length=100,db_column='LlavePrivada')
    llavepublica=models.CharField(max_length=100,db_column='LlavePublica')
    activo = models.IntegerField(null=True, db_column='Activo') # Field name made lowercase.
    class Meta:
        db_table = u'Tienda_Formapago'

class Zonas(models.Model):
    idzonas = models.AutoField(primary_key=True, db_column='idZonas') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre') # Field name made lowercase.
    descripcion = models.CharField(max_length=135, db_column='Descripcion') # Field name made lowercase.
    activo = models.IntegerField(null=True, db_column='Activo') # Field name made lowercase.
    tienda = models.ForeignKey(Tienda, db_column='Tienda') # Field name made lowercase.
    estados = models.TextField(db_column='Estados' ) # Field name made lowercase.
    class Meta:
        db_table = u'Zonas'


class Promociones(models.Model):
    idpromociones = models.AutoField(primary_key=True, db_column='idPromociones') # Field name made lowercase.
    codigo = models.CharField(max_length=135, db_column='Codigo' ) # Field name made lowercase.
    fechainicio = models.DateField(null=True, db_column='FechaInicio' ) # Field name made lowercase.
    fechafinal = models.DateField(null=True, db_column='FechaFinal' ) # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion' ) # Field name made lowercase.
    imagen = models.CharField(max_length=750, db_column='Imagen' ) # Field name made lowercase.
    stock = models.ForeignKey(Stock, db_column='Stock') # Field name made lowercase.
    class Meta:
        db_table = u'Promociones'

class Formaenvio(models.Model):
    idformaenvio = models.AutoField(primary_key=True, db_column='idFormaEnvio') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre' ) # Field name made lowercase.
    datos = models.TextField(db_column='Datos' ) # Field name made lowercase.
    logo = models.CharField(max_length=150, db_column='Logo' ) # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = u'FormaEnvio'


class Pedidos(models.Model):
    idpedidos = models.AutoField(primary_key=True, db_column='idPedidos') # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha') # Field name made lowercase.
    clientes = models.ForeignKey(Clientes, db_column='Clientes') # Field name made lowercase.
    stock = models.ForeignKey(Stock, db_column='Stock') # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    comentarios = models.TextField(db_column='Comentarios') # Field name made lowercase.
    status = models.CharField(max_length=135)
    direccionenvio = models.TextField(db_column='DireccionEnvio') # Field name made lowercase.
    estado = models.IntegerField(db_column='Estado') # Field name made lowercase.
    importe = models.DecimalField(decimal_places=2, max_digits=12, db_column='Importe') # Field name made lowercase.
    importeenvio = models.DecimalField(decimal_places=2, max_digits=12, db_column='ImporteEnvio')
    cpe = models.CharField(max_length=135, db_column='CPE') # Field name made lowercase.
    zonas = models.ForeignKey(Zonas, db_column='Zonas') # Field name made lowercase.
    formaenvio = models.ForeignKey(Formaenvio, db_column='FormaEnvio') # Field name made lowercase.
    class Meta:
        db_table = u'Pedidos'




class Categorias(models.Model):
    idcategorias = models.AutoField(primary_key=True, db_column='idCategorias') # Field name made lowercase.
    nombre = models.CharField(max_length=300, db_column='Nombre' ) # Field name made lowercase.
    descripcion = models.CharField(max_length=450, db_column='Descripcion' ) # Field name made lowercase.
    slug = AutoSlugField(populate_from='nombre',always_update=True,max_length=300)
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    stock = models.ForeignKey(Stock, db_column='Stock') # Field name made lowercase.
    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = u'Categorias'

class Productos(models.Model):
    idproductos = models.AutoField(primary_key=True, db_column='idProductos') # Field name made lowercase.
    nombre = models.CharField(max_length=750, db_column='Nombre') # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion') # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    precio = models.DecimalField(decimal_places=2, max_digits=12, db_column='Precio') # Field name made lowercase.
    unidad = models.ForeignKey(Unidades, db_column='Unidad') # Field name made lowercase.
    categorias = models.ForeignKey(Categorias, db_column='Categorias') # Field name made lowercase.
    def __unicode__(self):
        return self.nombre  
    class Meta:
        db_table = u'Productos'

class Galeria(models.Model):
    idgaleria = models.AutoField(primary_key=True, db_column='idGaleria') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre') # Field name made lowercase.
    archivo = models.CharField(max_length=150, db_column='Archivo') # Field name made lowercase.
    tipo = models.CharField(max_length=3, db_column='Tipo') # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    productos = models.ForeignKey(Productos, db_column='Productos') # Field name made lowercase.
    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = u'Galeria'



class ProductosPromociones(models.Model):
    productos = models.ForeignKey(Productos, db_column='Productos',primary_key=True) # Field name made lowercase.
    #promociones = models.ForeignKey(Promociones, db_column='Promociones',primary_key=True) # Field name made lowercase.
    promociones = models.ForeignKey(Promociones, db_column='Promociones')
    descuento = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='Descuento' ) # Field name made lowercase.
    cantidad = models.DecimalField(decimal_places=2, null=True, max_digits=6, db_column='Cantidad' ) # Field name made lowercase.
    class Meta:
        db_table = u'Productos_Promociones'

class PromocionesTipocliente(models.Model):
    promociones = models.ForeignKey(Promociones, db_column='Promociones') # Field name made lowercase.
    tipocliente = models.ForeignKey(Tipocliente, db_column='TipoCliente') # Field name made lowercase.
    class Meta:
        db_table = u'Promociones_Tipocliente'

class TiendaFormaenvio(models.Model):
    tienda = models.ForeignKey(Tienda, db_column='Tienda',primary_key=True) # Field name made lowercase.
    #formaenvio = models.ForeignKey(Formaenvio, db_column='FormaEnvio',primary_key=True) # Field name made lowercase.
    formaenvio = models.ForeignKey(Formaenvio, db_column='FormaEnvio') # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    class Meta:
        db_table = u'Tienda_Formaenvio'

class Paquetes(models.Model):
    idpaquetes = models.AutoField(primary_key=True, db_column='idPaquetes') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre' ) # Field name made lowercase.
    maximo = models.CharField(max_length=135, db_column='Maximo') # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    tienda = models.ForeignKey(Tienda, db_column='Tienda') # Field name made lowercase.

    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = u'Paquetes'


class PaquetesFormaenvio(models.Model):
    paquetes = models.ForeignKey(Paquetes, db_column='Paquetes',primary_key=True) # Field name made lowercase.
    #formaenvio = models.ForeignKey(Formaenvio, db_column='FormaEnvio',primary_key=True) # Field name made lowercase.
    formaenvio = models.ForeignKey(Formaenvio, db_column='FormaEnvio')
    #zonas = models.ForeignKey(Zonas, db_column='Zonas',primary_key=True) # Field name made lowercase.
    zonas = models.ForeignKey(Zonas, db_column='Zonas') # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    importe = models.DecimalField(decimal_places=2, null=True, max_digits=8, db_column='Importe') # Field name made lowercase.
    class Meta: 
        primary_keys=('paquetes', 'formaenvio', 'zonas') 
    def __unicode__(self):
        return self.paquetes
    class Meta:
        db_table = u'Paquetes_Formaenvio'

class PaquetesCategorias(models.Model):
    paquetes = models.ForeignKey(Paquetes, db_column='Paquetes',primary_key=True) # Field name made lowercase.
    #categorias = models.ForeignKey(Categorias, db_column='Categorias',primary_key=True) # Field name made lowercase.
    categorias = models.ForeignKey(Categorias, db_column='Categorias')
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    class Meta: 
        primary_key=('Paquetes','Categorias') 
    class Meta:
        db_table = u'Paquetes_Categorias'

class ImagenesProducto(models.Model):
    idimagenes_producto = models.AutoField(primary_key=True, db_column='idImagenes_producto') # Field name made lowercase.
    archivo = models.CharField(max_length=135, db_column='Archivo') # Field name made lowercase.
    prioridad = models.CharField(max_length=135)
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    productos = models.ForeignKey(Productos, db_column='Productos') # Field name made lowercase.
    class Meta:
        db_table = u'Imagenes_Producto'

class Extras(models.Model):
    idtable1 = models.AutoField(primary_key=True)
    concepto = models.CharField(max_length=135, db_column='Concepto' ) # Field name made lowercase.
    valor = models.DecimalField(decimal_places=2, null=True, max_digits=8, db_column='Valor' ) # Field name made lowercase.
    tipo = models.CharField(max_length=135 )
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    pedidos = models.ForeignKey(Pedidos, db_column='Pedidos') # Field name made lowercase.
    class Meta:
        db_table = u'Extras'

class Modelos(models.Model):
    idmodelos = models.AutoField(primary_key=True, db_column='idModelos') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre' ) # Field name made lowercase.
    precio = models.DecimalField(decimal_places=2, max_digits=8, db_column='Precio') # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion',blank=True) # Field name made lowercase.
    existencias = models.DecimalField(decimal_places=2, max_digits=7, db_column='Existencias')
    activo = models.IntegerField(db_column='Activo') 
    productos = models.ForeignKey(Productos, db_column='Productos') # Field name made lowercase.
    def __unicode__(self):
        return self.nombre
    class Meta:
        db_table = u'Modelos'

class PedidosProductos(models.Model):
    pedidos = models.ForeignKey(Pedidos, db_column='Pedidos') # Field name made lowercase.
    productos = models.ForeignKey(Productos, db_column='Productos') # Field name made lowercase.
    modelos = models.ForeignKey(Modelos, db_column='Modelos', primary_key=True) # Field name made lowercase.
    cantidad = models.DecimalField(decimal_places=2, max_digits=12, db_column='Cantidad') # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    class Meta:
        db_table = u'Pedidos_Productos'


class Cargos(models.Model):
    idcargo = models.CharField(primary_key=True, max_length=150, db_column='idCargo') # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha') # Field name made lowercase.
    status = models.CharField(max_length=3)
    importe = models.IntegerField(db_column='Importe') # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    formapago = models.ForeignKey(Formapago, db_column='FormaPago') # Field name made lowercase.
    pedidos = models.ForeignKey(Pedidos, db_column='Pedidos') # Field name made lowercase.
    def __unicode__(self):
        return self.idcargo
    class Meta:
        db_table = u'Cargos'

class Referencia(models.Model):
    idreferencia = models.AutoField(primary_key=True, db_column='idReferencia') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre', blank=True) # Field name made lowercase.
    valor = models.CharField(max_length=135, db_column='Valor', blank=True) # Field name made lowercase.
    cargos = models.ForeignKey(Cargos, db_column='Cargos') # Field name made lowercase.
    class Meta:
        db_table = u'Referencia'
        

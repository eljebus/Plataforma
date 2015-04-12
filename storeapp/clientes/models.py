# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Cliente(models.Model):
    idclientes = models.AutoField(primary_key=True, db_column='idClientes') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre') # Field name made lowercase.
    telefono = models.CharField(max_length=135, db_column='Telefono') # Field name made lowercase.
    mail = models.CharField(max_length=135, db_column='Mail') # Field name made lowercase.
    sexo = models.CharField(max_length=3, db_column='Sexo') # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha') # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    class Meta:
        db_table = u'Cliente'

class ClientesTiendas(models.Model):
    clientes = models.ForeignKey(Cliente, db_column='Clientes') # Field name made lowercase.
    tiendas = models.IntegerField(primary_key=True)
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    class Meta:
        db_table = u'Clientes__tiendas'

class Contrato(models.Model):
    idcontrato = models.AutoField(primary_key=True, db_column='idContrato') # Field name made lowercase.
    inicio = models.DateField(null=True, db_column='Inicio', blank=True) # Field name made lowercase.
    fin = models.DateField(null=True, db_column='Fin', blank=True) # Field name made lowercase.
    fecha = models.DateField(null=True, db_column='Fecha', blank=True) # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    tienda=models.IntegerField(db_column='Tienda')
    clientes_idclientes = models.ForeignKey(Cliente, db_column='Clientes_idClientes') # Field name made lowercase.
    class Meta:
        db_table = u'Contrato'

class Pagos(models.Model):
    idpagos = models.AutoField(primary_key=True, db_column='idPagos') # Field name made lowercase.
    forma = models.CharField(max_length=450, db_column='Forma') # Field name made lowercase.
    monto = models.DecimalField(decimal_places=2, max_digits=8, db_column='Monto') # Field name made lowercase.
    fecha = models.DateField(null=True, db_column='Fecha', blank=True) # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    contrato = models.ForeignKey(Contrato, db_column='Contrato') # Field name made lowercase.
    class Meta:
        db_table = u'Pagos'

class Privilegios(models.Model):
    idprivilegios = models.AutoField(primary_key=True, db_column='idPrivilegios') # Field name made lowercase.
    nivel = models.CharField(max_length=135, db_column='Nivel', blank=True) # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion', blank=True) # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    
    contrato = models.ForeignKey(Contrato, db_column='Contrato')
    class Meta:
        db_table = u'Privilegios'

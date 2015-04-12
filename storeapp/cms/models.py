# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Cms(models.Model):
    idcms = models.AutoField(primary_key=True, db_column='idCms') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre') # Field name made lowercase.
    descripcion = models.CharField(max_length=450, db_column='Descripcion') # Field name made lowercase.
    imagen = models.CharField(max_length=135, db_column='Imagen') # Field name made lowercase.
    activo = models.IntegerField(db_column='Activo') # Field name made lowercase.
    estilos = models.CharField(max_length=150)

    contenido = models.CharField(max_length=150)
    class Meta:
        db_table = u'Cms'

class Conjunto(models.Model):
    idconjunto = models.AutoField(primary_key=True, db_column='idConjunto') # Field name made lowercase.
    tienda = models.IntegerField(db_column='Tienda') # Field name made lowercase.
    fecha = models.DateField(null=True, blank=True)
    activo = models.IntegerField(null=True, db_column='Activo', blank=True) # Field name made lowercase.
    cms = models.ForeignKey(Cms, db_column='Cms') # Field name made lowercase.
    class Meta:
        db_table = u'Conjunto'

class Secciones(models.Model):
    idsecciones = models.AutoField(primary_key=True, db_column='idSecciones') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre') # Field name made lowercase.
    titulo = models.CharField(max_length=135, db_column='Titulo') # Field name made lowercase.
    contenido = models.CharField(max_length=750)
    activo = models.IntegerField(null=True, db_column='Activo', blank=True) # Field name made lowercase.
    conjunto = models.ForeignKey(Conjunto, db_column='Conjunto') # Field name made lowercase.
    class Meta:
        db_table = u'Secciones'

class Subsecciones(models.Model):
    idsubsecciones = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=135, db_column='Nombre', blank=True) # Field name made lowercase.
    titulo = models.CharField(max_length=135, db_column='Titulo', blank=True) # Field name made lowercase.
    contenido = models.TextField(db_column='Contenido', blank=True) # Field name made lowercase.
    secciones = models.ForeignKey(Secciones, db_column='Secciones') # Field name made lowercase.
    class Meta:
        db_table = u'Subsecciones'

class Imagenes(models.Model):
    idimagenes = models.AutoField(primary_key=True, db_column='idImagenes') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre', blank=True) # Field name made lowercase.
    archivo = models.CharField(max_length=450, db_column='Archivo', blank=True) # Field name made lowercase.
    tipo = models.CharField(max_length=135, db_column='Tipo', blank=True) # Field name made lowercase.
    activo = models.IntegerField(null=True, db_column='Activo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Imagenes'

class GaleriaCms(models.Model):
    idgaleria = models.AutoField(primary_key=True, db_column='idGaleria') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre', blank=True) # Field name made lowercase.
    activo = models.IntegerField(null=True, db_column='Activo', blank=True) # Field name made lowercase.
    subsecciones = models.ForeignKey(Subsecciones, db_column='subsecciones')
    class Meta:
        db_table = u'Galeria'

class GaleriaImagenes(models.Model):
    galeria = models.ForeignKey(GaleriaCms, db_column='GaleriaCms') # Field name made lowercase.
    imagenes = models.ForeignKey(Imagenes, db_column='Imagenes') # Field name made lowercase.
    activo = models.IntegerField(null=True, db_column='Activo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Galeria_Imagenes'

class Plugin(models.Model):
    idplugin = models.AutoField(primary_key=True, db_column='idPlugIn') # Field name made lowercase.
    nombre = models.CharField(max_length=135, db_column='Nombre', blank=True) # Field name made lowercase.
    tipo = models.CharField(max_length=135, db_column='Tipo', blank=True) # Field name made lowercase.
    archivo = models.CharField(max_length=135, db_column='Archivo', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Plugin'

class SubseccionesPlugin(models.Model):
    subsecciones = models.ForeignKey(Subsecciones, db_column='subsecciones')
    plugin = models.ForeignKey(Plugin, db_column='PlugIn') # Field name made lowercase.
    class Meta:
        db_table = u'Subsecciones_Plugin'

class Propiedades(models.Model):
    idpropiedades = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=135, blank=True)
    valor = models.CharField(max_length=300, blank=True)
    secciones = models.ForeignKey(Secciones, db_column='Secciones') # Field name made lowercase.
    class Meta:
        db_table = u'Propiedades'

class Propiedadessubsecciones(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=135, blank=True)
    valor = models.CharField(max_length=135, db_column='Valor', blank=True) # Field name made lowercase.
    propiedadessubseccionescol = models.CharField(max_length=135, db_column='PropiedadesSubseccionescol', blank=True) # Field name made lowercase.
    subsecciones = models.ForeignKey(Subsecciones, db_column='subsecciones')
    class Meta:
        db_table = u'PropiedadesSubsecciones'




#---------------------------------------



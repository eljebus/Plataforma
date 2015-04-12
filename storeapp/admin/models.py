from django.db import models
from django.contrib.auth.models import User



class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True) # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=140, blank=True) # Field name made lowercase.
    correo = models.EmailField(db_column='correo', max_length=140, blank=True) # Field name made lowercase.
    negocio= models.CharField(db_column='Negocio', max_length=145, blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    Fecha = models.DateTimeField(db_column='Fecha',auto_now_add=True)
    class Meta:
        db_table = 'Usuario'

    def __unicode__(self):
        return self.idusuario


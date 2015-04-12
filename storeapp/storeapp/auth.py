from clientes.models import*
from store.models import Administrador
from django.contrib.sessions.backends.db import SessionStore
from django.core.exceptions import *


class auth():

	def validarUsuario(self,user,password):
		self.s = SessionStore()
		contador=Administrador.objects.filter(login__exact=user)  
		if contador.count()>0:
			m = Administrador.objects.get(login__exact=user)
			if m.password == password:
				return True
			else:
				return False

	

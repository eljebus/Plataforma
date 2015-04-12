
class Funciones():
	def validarForm(self,formulario):
		valor={"vacio":False,"valores":''}
		for clave in formulario:

			if(len(formulario[clave])==0):
				
				valor['vacio']=True
				valor['valores']+=clave+" "

		return valor






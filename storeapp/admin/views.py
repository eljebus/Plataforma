# -*- coding: utf-8 -*-
#from unicode import unicode
from django.shortcuts import render_to_response
from django.db import IntegrityError
from django.template.context import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from funciones import *
from ajax import *
from models import *
from store.models import *
from cms.models import *
from store.views import getTotalCesta, getDatos
from forms import *
from django.core.mail import *
import urllib2 
import urllib
import json
from django.shortcuts import redirect
from datetime import date, timedelta
from django.core.exceptions import *
from django.contrib.sites.models import Site
import os
from django.conf import settings
from django.db import transaction
from django.contrib.sites.models import Site
import uuid

# Create your views here.
fun=Funciones()



def registroUsuarios(request):
	if request.POST:
		form = UsuarioForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
	else:
		form=UsuarioForm()

	return render_to_response('registro.html',context_instance=RequestContext(request,locals()))



def home(request):
	

	datos={'Descripcion':'Proximamente'}	

	site = Site.objects.get_current()
	render=''


	if site.name== 'wido.com.mx':
		render = 'index.html'

	else:
		try:
		    getDatos(datos,request)

		    productos = Productos.objects.all().extra(select={'nombre':'Productos.Nombre','archivo':'Galeria.Archivo'}).filter(galeria__tipo="A").filter(categorias__in=datos['categorias']).filter(activo=1).order_by('-idproductos').filter(activo=1).distinct()[0:8]
		    
		    current_site 		= Site.objects.get_current()

		    datos['productos']	= productos
		    datos['anuncios']	= datos['tienda'].anuncios_set.all()
		    render='indexTienda.html'
		    
	   	except Exception, e:
			raise e
   	

	return render_to_response(render,datos,context_instance=RequestContext(request,locals()))

def registro(request):
	dic={'Error':True} 
	if request.is_ajax():
		if request.method == 'POST':
			form = UsuarioForm(request.POST)
			if form.is_valid():
				form.save()
				dic['Error']=False;
				return HttpResponse(
					json.dumps(dic),
					content_type='application/json;charset=utf8'
					)
	else:
		raise Http404

def blog(request):
	datos={}
	template='articulos.html'
	tiendas=Tienda.objects.filter(activo=1).exclude(logo='Subir logo')[0:2]
	datos['tiendas']=tiendas
	return render_to_response(template,datos,context_instance=RequestContext(request,locals()))

def terminos(request):
	datos={}
	template='terminos.html'
	tiendas=Tienda.objects.filter(activo=1)[0:2]
	datos['tiendas']=tiendas
	return render_to_response(template,datos,context_instance=RequestContext(request,locals()))



def clientes(request):
	
	return render_to_response('clientes.html',context_instance=RequestContext(request,locals()))

def Galeria(request):
	todas=Tienda.objects.filter(activo=1).exclude(logo='Subir logo')[0:10]
	tiendas=Tienda.objects.filter(activo=1).exclude(logo='Subir logo')[0:2]
	dominios=Site.objects.filter(tienda__activo=1)
	dic={}
	dic['tiendas']=tiendas
	dic['dominios']=dominios
	
	dic['todas']=todas
	return render_to_response('galeria.html',context_instance=RequestContext(request,dic))

def Curso(request):
	tiendas=Tienda.objects.filter(activo=1).exclude(logo='Subir logo')[0:2]
	dominios=Site.objects.filter(tienda__activo=1)
	dic={}
	dic['tiendas']=tiendas
	dic['dominios']=dominios
	
	return render_to_response('curso.html',context_instance=RequestContext(request,dic))



from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def registroCurso(request):
	dic={'Error':True} 
	if request.is_ajax():
		if request.POST:
			from clientes.models import Cliente,ClientesTiendas,Contrato
			try:
				Cliente.objects.get(mail=request.POST['mail'])
			except ObjectDoesNotExist:
				cliente=Cliente()
				cliente.nombre=request.POST['nombreCliente']
				cliente.telefono='Desconocido'
				cliente.mail=request.POST['mail']
				cliente.sexo='N'
				cliente.fecha=date.today()
				cliente.activo=0
				cliente.save()

			dic['Error']=False;
			return HttpResponse(
				json.dumps(dic),
				content_type='application/json;charset=utf8'
				)
	else:
		raise Http404

def login(request,boolean):
	datos={'Usuario':''}
	if boolean=='False':
		datos['Usuario']='Usuario no válido'

	tiendas=Tienda.objects.filter(activo=1).exclude(logo='Subir logo')[0:2]
	
	datos['tiendas']=tiendas	

	return render_to_response('ingreso.html',datos,context_instance=RequestContext(request,locals()))

def planes(request):
	datos={'Usuario':''}

	tiendas=Tienda.objects.filter(activo=1)[0:2]
	
	datos['tiendas']=tiendas	

	return render_to_response('planes.html',datos,context_instance=RequestContext(request,locals()))

def crearTienda(request):
	datos={}
	if request.is_ajax():
		if request.POST:
			from clientes.models import Cliente,ClientesTiendas,Contrato,Privilegios
			import re
				
			if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',request.POST['mail'].lower()) and re.match('|^[a-zA-Z]*$|',request.POST['subdominio'].lower()):
				try:
					site = Site.objects.get(domain=request.POST['subdominio']+'.mindoncloud.com')
					datos['Error']=True
					datos['letras']='La tienda ya existe intena con otro Nombre'
				except ObjectDoesNotExist:
					try:
						cliente=Cliente.objects.get(mail__exact=request.POST['mail'])
						print('test')
						datos['Error']=True
						datos['letras']='Correo no válido1'
					except ObjectDoesNotExist:
						try:
							Tienda.objects.get(nombre=request.POST['nombreTienda'],activo=1)
							datos['Error']=True
							datos['letras']='Nombre de tienda en uso'
						except ObjectDoesNotExist:
							try:
								Site.objects.get(domain=request.POST['subdominio']+'.wido.mx')
								datos['Error']=True
								datos['letras']='Direccion de tienda en uso'
							except ObjectDoesNotExist:
								datos['Error']=False

					if datos['Error'] == False:
						from datetime import date, timedelta


						url =  urllib.urlopen("https://api.digitalocean.com/v1/domains/new?client_id=30c316cd106ea8d3aec887283db8dd24&api_key=972292751ed197d894365b2df49c771e&name="+request.POST['subdominio']+".wido.com.mx&ip_address=104.236.24.225")

						url =  urllib.urlopen("https://api.digitalocean.com/v1/domains/new?client_id=30c316cd106ea8d3aec887283db8dd24&api_key=972292751ed197d894365b2df49c771e&name=www."+request.POST['subdominio']+".wido.com.mx&ip_address=104.236.24.225")

						site=Site()
						site.domain=request.POST['subdominio']+'.wido.com.mx'
						site.name=request.POST['subdominio']
						site.save()


						cliente=Cliente()
						cliente.nombre=request.POST['nombreCliente']
						cliente.telefono='Desconocido'
						cliente.mail=request.POST['mail']
						cliente.sexo='N'
						cliente.fecha=date.today()
						cliente.usuario=0
						cliente.activo=1
						cliente.save()

						admin=Administrador()
						admin.nombre=request.POST['nombreCliente']
						admin.login=request.POST['subdominio']+str(uuid.uuid4().hex)[:3]
						admin.password=str(uuid.uuid4().hex)[:8]
						admin.cliente=str(cliente.idclientes)
						admin.activo=1
						admin.save()

						tienda=Tienda()
						tienda.nombre=request.POST['nombreTienda']
						tienda.rfc='RFC Desconocido'
						tienda.logo='Subir logo'
						tienda.ubicacion='Domicilio Desconocido'
						tienda.direccion='Domicilio Desconocido'
						tienda.mail='mail Desconocido'
						tienda.telefono='telefono desconocido'
						tienda.descripcion='Desconocido'
						tienda.activo=0
						tienda.administrador=admin
						tienda.site_id=int(site.id)
						tienda.save()

						parametros={
						    'mailreceptor':request.POST['mail'],
						    'mailemisor':'contacto@wido.com.mx',
						    'asunto':'Bienvenido a WIDO',
						    'texto':'<h1>Nuevo cliente</h1> <p>Nuevo Cliente con plan simple</p><p>Nombre '+str(cliente.nombre)+'<br>Datos de acceso:<br> usuario:'+admin.login+'<br>clave: '+admin.password
						}

						setMensaje(parametros)

						stock=Stock()
						stock.fecha=date.today()
						stock.descripcion='Stock de la tienda '+request.POST['nombreTienda']
						stock.tienda=tienda
						stock.save();

						tp=Tipocliente()
						tp.nombre='Casual'
						tp.descripcion='Cliente Casual de tienda '+unicode(request.POST['subdominio'])
						tp.prioridad=1
						tp.stock_idstock=stock
						tp.save()


						contrato=Contrato()
						contrato.inicio=date.today()
						current_date=date.today()
						"""new_month=divmod(current_date.month-1+1, 12)
						new_month+=1
						current_date=current_date.replace(year=current_date.year+carry, month=new_month)"""


						contrato.fin=date.today()+timedelta(days=7)
						contrato.fecha=date.today()
						contrato.tienda=str(tienda.idtienda)
						contrato.clientes_idclientes=cliente
						contrato.activo=1
						contrato.save()

						privilegio=Privilegios()
						#privilegio.nivel=request.POST['planes']
						privilegio.nivel='Bronce'
						privilegio.descripcion='Conocida'
						privilegio.activo=1
						privilegio.contrato=contrato
						privilegio.save()


						ct=ClientesTiendas()
						ct.clientes=cliente
						ct.tiendas=str(tienda.idtienda)
						ct.activo=1
						ct.save();

						conjunto=Conjunto()
						conjunto.tienda=int(tienda.idtienda)
						conjunto.fecha=date.today()
						conjunto.activo=1
						conjunto.cms=Cms.objects.get(idcms=1)
						conjunto.save()

						secciones=Secciones()
						secciones.nombre='Pie'
						secciones.titulo='Pie de Pagina'
						secciones.contenido='plantilla1/footer.html'
						secciones.activo=1
						secciones.conjunto=conjunto
						secciones.save()

						secciones=Secciones()
						secciones.nombre='Cabecera'
						secciones.titulo='Cabecera de Pagina'
						secciones.contenido='plantilla1/header.html'
						secciones.activo=1
						secciones.conjunto=conjunto
						secciones.save()

						secciones=Secciones()
						secciones.nombre='Cuerpo'
						secciones.titulo='Cuerpo de Pagina'
						secciones.contenido='Conocido'
						secciones.activo=1
						secciones.conjunto=conjunto
						secciones.save()


						os.mkdir('/opt/wido/Plataforma/storeapp/static/imagenes/tiendas/'+unicode(request.POST['nombreTienda']).replace(' ','-'))


						#parametros={
					    #    'mailreceptor':'jesuscervantes82@hotmail.com',
					    #    'mailemisor':request.POST['mail'],
					    #    'asunto':'Nuevo Cliente',
					    #    'texto':'<h1>Nuevo cliente</h1> <p>Nuevo Cliente con plan simple</p><p>Nombre '+str(cliente.nombre)+'</p><p>Referencia '+str(cliente.idclientes)+'</p>',
					    #    }
						#setMensaje(parametros)
						#plan=request.POST['planes']
						#total=0
						#if plan == 'Bronce':
						#	total=200
						#elif plan=='Plata':
						#	total=300
						#else: 
						#	total=400

							
						#parametros={
						#        'mailreceptor':request.POST['mail'],
						#        'mailemisor':'ventas@wido.com.mx',
						#        'asunto':'Nuevo Cliente',
						#        'texto':'<!DOCTYPE html> <html lang="es"> <style type="text/css"> h1 {font-size: 2.7em; margin: 0; } h2 {font-size: 2em; } ul {list-style: none; width: 80%; margin-left: 25px; } #todo {padding: 40px; width: 800px; } #logo {width: 25%; height: 300px; display: inline-block; margin-right: 32px; } #logo img {width: 100%; } #derecha {width: 70%; height: auto; display: inline-block; vertical-align: top; } #derecha img {width: 60%; } #total {font-size:2em; font-weight: bold; } #nota {font-size: 18px; } #contenedor-total {margin-left: 40px; margin-bottom: 30px; margin-top: 20px; } .etiqueta {font-size: 18px; } </style> <head> <meta charset="utf-8" /> <title>Pago bancario</title> </head> <body> <header> </header> <div id="todo"> <div id="logo"> <img src="http://subdominios.wido.mx/wido.png"> </div> <div id="derecha"> <h1>Agradecemos tu preferencia</h1> <h2>Informaci&oacute;n de pago</h2> <img src="http://proyectopuente.com.mx/Content/images/posts/banamex.gif"> <ul> <li> <label class="etiqueta" >Beneficiario: Juan Perez</label> </li> <li> <label class="etiqueta" >Sucursal: 0706</label> </li> <li> <label class="etiqueta" >Cuenta: 2331512</label> </li> <li> <label class="etiqueta" >Clabe Interbancaria: 002357070623315125</label> </li> <li> <label class="etiqueta" >Referencia: '+str(cliente.idclientes)+'</label> </li> </ul> </div> <div id="contenedor-total"> <label id="total">Total a pagar: $'+str(total)+'.00</label> </div> <p id="nota"> Nota: Para poder identificar tu pago es importante coloques el numero de referencia a tu deposito. <br> Los pagos salvo buen cobro demoran 72 horas h&aacute;biles. </p> </div> <footer> </footer> </body> </html>',
						#        }

						#setMensaje(parametros)"""

						

						

						#params = urllib.urlencode({'user':'widomx','clave':'30UmjCz90m','subdominio':request.POST['subdominio']}) 
						#url=urllib.urlopen("http://subdominios.wido.mx/crear.php",params)
						
						
					

						
			else:
				datos['Error']=True
				datos['letras']='Correo inválido'
				
				

			return HttpResponse(
					json.dumps(datos),
					content_type='application/json;charset=utf8'
					)
	else:
		raise Http404


def contacto(request):
	dic={'Error':True} 
	if request.is_ajax():
		if request.POST:
			email = EmailMessage(request.POST['Nombre'],
								 request.POST['Negocio']
								 +' Mensaje: '
								 +request.POST['mensaje'], 
								 to = ['jesuscervantes82@hotmail.com'])
			email.send()
			dic['Error']=False;
			return HttpResponse(
				json.dumps(dic),
				content_type='application/json;charset=utf8'
				)
	else:
		raise Http404


def error404(request):
 	return render_to_response('index.html')

def Correo(request):
    dic={}
    if request.is_ajax():
        if request.POST:
		try:
			params2 = {
					'asunto':'Comentario',
			        'mailreceptor':'jesuscervantes82@hotmail.com',
			        'mailemisor':request.POST['data[e-mail]'],
			        'texto':'<h2>'+request.POST['data[name]']+'</h2><p>'+request.POST['data[mensaje]']+'</p>',
			        }

			setMensaje(params2)

			dic['Error']='false'

		except Exception, e:
			dic['Error']='true'
		return HttpResponse(
		    json.dumps(dic),
		    content_type='application/json;charset=utf8') 
			

    else:
        raise Http404

def setMensaje(parametros):
    try:
    	from django.core.mail import send_mail

    	send_mail(parametros['asunto'], 
		          parametros['texto'], 
		          parametros['mailemisor'],
		          [parametros['mailreceptor']])

    except Exception, e:
        return e
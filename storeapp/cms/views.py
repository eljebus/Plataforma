# -*- coding: utf-8 -*-
from unidecode import unidecode
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404,HttpRequest
from django.db.models import Q
from models import *
from store.models import *
from clientes.models import *
from storeapp.auth import auth
from storeapp.funciones import Funciones
import json
from json import JSONEncoder
from datetime import datetime
from django.core.paginator import *
import os
from storeapp import settings
from django.db import connection, transaction, DatabaseError, IntegrityError
from django.core.exceptions import *
from datetime import date, timedelta
# no permitir javascript


from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
import re

register = template.Library()

@register.filter
@stringfilter
def stripjs(value):
    stripped = re.sub(r'<script(?:\s[^>]*)?(>(?:.(?!/script>))*</script>|/>)', \
                      '', force_unicode(value), flags=re.S)
    return mark_safe(stripped)


#test


autenticar=auth()
fun=Funciones()
seccionesNombre=["Pie",'Cabecera','Cuerpo']
cursor = connection.cursor()



def login(request):
	redirect='/ingresar/False/'
	if request.POST:	
		request.session["user"] =autenticar.validarUsuario(request.POST['Nombre'],request.POST['Contrasena'])
		if request.session["user"]==True:

			admin=Administrador.objects.get(login__exact=request.POST['Nombre'])
			print admin

			tienda=Tienda.objects.get(administrador__exact=admin.idadministrador)

			request.session['habil']=''
			print str(admin.cliente)
			try:
				contrato=Contrato.objects.get(clientes_idclientes=str(admin.cliente),fin__gt= date.today(),tienda=str(tienda.idtienda))
			except ObjectDoesNotExist:
				contrato=Contrato.objects.get(clientes_idclientes=str(admin.cliente),tienda=str(tienda.idtienda))

				request.session['habil']="<label class='icon-sad'></label> Tu tienda Caducó el dia "+str(contrato.fin)

			stock=Stock.objects.get(tienda__exact=tienda.idtienda)

			request.session["idadministrador"]=admin.idadministrador

			request.session["cliente"]=admin.cliente

			request.session['tienda']=tienda


			request.session['stockAdmin']=stock

			redirect='/pedidosPanel/Pagado/'



	return HttpResponseRedirect(redirect)

def adminArea(request,status):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	if request.POST:
		variable=request.POST['buscar']
		pedidos=Pedidos.objects.filter(idpedidos__contains=variable,
										stock=request.session['stockAdmin'],
										activo=1 ).order_by('-idpedidos')
	else:
		pedidos=Pedidos.objects.filter(status=status,
										activo=1,
										stock=request.session['stockAdmin']
										).order_by('-idpedidos')

	cliente=getUser(request.session["cliente"])
	paginator = Paginator(pedidos, 15)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		fp = paginator.page(page)
	except (EmptyPage, InvalidPage):
		fp = paginator.page(paginator.num_pages)


	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':'Pedidos',
	 	 'pedidos':fp,
	 	 'status':status,
	 	 'ver':'none'}

	dic['accion']='/pedidosPanel/Busqueda/'


	return render_to_response('pedidos.html',context_instance=RequestContext(request,dic))

def getNivel(request):
	try:
		categorias=Categorias.objects.filter(stock=request.session['stockAdmin'])
		cantidad=Productos.objects.filter(categorias__in=categorias,activo=1).count()

		tienda=request.session['tienda']

		miContrato=Contrato.objects.get(tienda=str(tienda.idtienda),activo=1,)

		privilegio=Privilegios.objects.get(contrato=miContrato,activo=1)

		cantidadAprobada=0

		if str(privilegio.nivel)=='Bronce':
			cantidadAprobada=50
		elif str(privilegio.nivel)=='Plata':
			cantidadAprobada=150
		elif str(privilegio.nivel)=='Oro':
			cantidadAprobada=400

		if cantidad <= (cantidadAprobada-1):
			return True
		else:
			return False

	except ObjectDoesNotExist:
		return False

def addProduct(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	if not getNivel(request):
		return HttpResponseRedirect('/productos/')

	test=''
	cliente=getUser(request.session["cliente"])
	unidades=Unidades.objects.values()
	categorias=Categorias.objects.all().filter(stock=request.session['stockAdmin'],activo=1)
	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':'Agregar Productos',
	 	 'ver':'none',
	 	 'unidades':unidades,
	 	 'categorias':categorias,
	 	 'action':'/producto/nuevo/',
	 	 'required':'required'
	 	 }
	if request.POST:


		valores=fun.validarForm(request.POST)

		if(valores['vacio']==True):
			dic['letrero']=valores['valores']+' vacio'
		else:
			categoria=Categorias.objects.get(nombre__exact=request.POST['categoria'],stock=request.session['stockAdmin'].idstock)
			unidad=Unidades.objects.get(nombre=request.POST['unidad'])

			try:
				
				#compruebo si el producto ya existe y solo lo actualizo, elimino los modelos que existian
				producto=Productos.objects.get(nombre=request.POST['nombre'],categorias=categoria)
				objetcUpdate(producto,request.POST)
				producto.activo=1
				producto.save()

				#se actualiza el modelo del preoducto con las existencias
				modeloProducto=Modelos.objects.get(nombre=str(producto.nombre),productos__exact=producto)
				modeloProducto.save()
				#Si existen modelos del producto los desactiva para poner los nuevos
				Modelos.objects.filter(productos__exact=producto).exclude(nombre=str(producto.nombre)).update(activo='0')
				#elimino las imagenes del producto
				imagenes=Galeria.objects.all().filter(productos__exact=producto)
				for i in imagenes:
					try:
						os.unlink(os.path.join(settings.STATIC_URL, i.archivo))
					except Exception, e:
						print "error " + e.message
					i.delete()

			except ObjectDoesNotExist:
				#si el producto no existe se crea de nuevo
				producto= Productos()

				objetcUpdate(producto,request.POST)

				producto.categorias=categoria
				producto.unidad=unidad
				producto.activo=1
				producto.save()

				modeloProducto=Modelos()
				modeloProducto.nombre=request.POST['nombre']
				modeloProducto.precio=0
				modeloProducto.descripcion=request.POST['descripcion']
				modeloProducto.productos=producto
				if not request.POST.get('existencias',False):
					modeloProducto.existencias=0
				else:
					modeloProducto.existencias=request.POST['existencias']
				modeloProducto.activo=1
				modeloProducto.save()


			existenciasProducto=0
			for e in request.POST:
				if 'nombreModelo_' in str(e): 	
					test=e
					test=test.replace('nombreModelo_','')	
					try:
						#verifica si el modelo existe y se actualiza
						modelo=Modelos.objects.get(nombre=request.POST['nombreModelo_'+test],productos=producto)
						modelo.activo=1 
						modelo.precio=request.POST['precioModelo_'+test]
						modelo.existencias=request.POST['existenciasModelo_'+test]
						modelo.save()
						existenciasProducto=existenciasProducto+modelo.existencias

					except ObjectDoesNotExist:
						#si no existe el modelo se crea

						modelo=Modelos()
						modelo.nombre=request.POST['nombreModelo_'+test]
						modelo.precio=request.POST['precioModelo_'+test]
						modelo.descripcion=request.POST['descripcionModelo_'+test]
						modelo.productos=producto
						modelo.existencias=request.POST['existenciasModelo_'+test]
						modelo.activo=1
						modelo.save()
						existenciasProducto=existenciasProducto+int(modelo.existencias)

			if existenciasProducto > 0:

				#se guardan las existencias del producto en base a los modelos
				modeloProducto.existencias=existenciasProducto
				modeloProducto.save()

			archivos=request.FILES.getlist('files[]')

			handle_uploaded_file(archivos,unidecode(request.session['tienda'].nombre).replace(' ','-'))

			contador=0
			for image in request.FILES.getlist('files[]'):
				if contador<=3:
					imagen=Galeria()
					imagen.nombre=image.name
					imagen.archivo='imagenes/tiendas/'+unidecode(unicode(request.session['tienda'].nombre)).replace(' ','-')+'/'+unidecode(unicode(image.name)).replace(' ','-')


					if contador==0:
						imagen.tipo='A'
					else:
						imagen.tipo='B'

					imagen.activo=1
					imagen.productos=producto
					imagen.save()
					contador=contador+1
			dic['letrero']='Producto Agregado'
			getErrorLabel(False,dic)



	return render_to_response('productosAdd.html',context_instance=RequestContext(request,dic))

def listProducts(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')

	cliente=getUser(request.session["cliente"])
	categorias=Categorias.objects.all().filter(stock=request.session['stockAdmin'].idstock,activo=1)
	if request.POST:
		variable=request.POST['buscar']
		productos=Productos.objects.all().filter(Q(nombre__contains=variable) | Q(idproductos__startswith=variable),categorias__in=categorias,activo=1).filter(activo=1).order_by('-idproductos')
	else:

		productos=Productos.objects.all().filter(categorias__in=categorias).filter(activo=1).order_by('-idproductos')

	paginator = Paginator(productos, 15)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		fp = paginator.page(page)
	except (EmptyPage, InvalidPage):
		fp = paginator.page(paginator.num_pages)

	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':'Productos',
	 	 'ver':'none',
	 	 'productos':fp,
	 	 }
	if not getNivel(request):
		dic['limite']='<br><label class="icon-sad"></label> Has llegado al Limite de Productos solicita subir de Nivel'

	dic['accion']='/productos/'

	"""
	inicio=int(pagina*15)
	fin=int(pagina*15)+14
	contador=Productos.objects.filter(categorias__in=categorias)
	
	paginas=paginar(contador.count())

	productos=Productos.objects.all().filter(categorias__in=categorias)[inicio:fin]

	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['logo'],
	 	 'titulo':'Productos',
	 	 'ver':'none',
	 	 'productos':productos,
	 	 'paginas':paginas
	 	 }"""


	return render_to_response('productos.html',context_instance=RequestContext(request,dic))

def handle_uploaded_file(f,tienda):	
	for upfile in f:
		filename = upfile.name
		with open('/opt/wido/Plataforma/storeapp/static/imagenes/tiendas/'+str(tienda).replace(' ','-').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n')+'/'+unidecode(filename).replace(' ','-'), 'wb+') as destination:
			for chunk in upfile.chunks():
				destination.write(chunk)

def listCategory(request):
	dic={}
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')

	cliente=getUser(request.session["cliente"])
	categorias=Categorias.objects.all().filter(stock=request.session['stockAdmin'],activo=1)

	dic={'Usuario':cliente.nombre,
 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
 	 'titulo':'Categorías',
 	 'ver':'none',
 	 }
	dic['categorias']=categorias
	return render_to_response('categorias.html',context_instance=RequestContext(request,dic))

def addCategory(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])
	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':'Agregar Categoría',
	 	 'ver':'none',
	 	 'accion':'/categoria/nueva/'
	 	 }
	if request.POST:

		valores=fun.validarForm(request.POST)

		if(valores['vacio']==True):
			dic['letrero']=valores['valores']+' vacio'
		else:

				try:
					categoria=Categorias.objects.get(nombre=request.POST['nombre'],stock=request.session['stockAdmin'])
					categoria.descripcion=request.POST['descripcion']
					categoria.activo=1
					categoria.save()
				except ObjectDoesNotExist:
					try:
						categoria=Categorias()

						objetcUpdate(categoria,request.POST)

						categoria.stock=request.session['stockAdmin']
						categoria.activo=1
						categoria.save()
						dic['letrero']='Categoría Agregada'
						getErrorLabel(False,dic)
					except Exception, e:
						dic['letrero']='Oops! ocurrio un error'
						getErrorLabel(True,dic)

	return render_to_response('categoriasAdd.html',context_instance=RequestContext(request,dic))

def modifyCategory(request,idcat):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])
	categoria=Categorias.objects.get(idcategorias=idcat)

	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':'Modificar Categoría',
	 	 'categoria':categoria,
	 	 'ver':'none',
	 	 'accion':'/categoria/'+str(categoria.idcategorias)+'/'
	 	 }
	if request.POST:

		valores=fun.validarForm(request.POST)

		if(valores['vacio']==True):
			dic['letrero']=valores['valores']+' vacio'
			print 'paso 1'
		else:

				try:
					categoria.nombre=request.POST['nombre']
					categoria.descripcion=request.POST['descripcion']
					categoria.activo=1
					categoria.save()
					dic['categoria']=categoria
					getErrorLabel(False,dic)
					dic['letrero']='Cambios Guardados'
				except Exception, e:
					dic['letrero']='Oops! ocurrio un error'
					getErrorLabel(True,dic)

	return render_to_response('categoriasAdd.html',context_instance=RequestContext(request,dic))

def addAnuncio(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])
	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':'Agregar Anuncio',
	 	 'ver':'none'}
	if request.POST:
		valores=fun.validarForm(request.POST)

		if(valores['vacio']==True):
			dic['letrero']=valores['valores']+' vacio'
		else:
			try:
				try:
					Anuncios.objects.get(tienda=request.session['tienda'],nombre=request.POST['nombre'])
					objetcUpdate(anuncio,request.POST)

					archivos=request.FILES.getlist('file')

					handle_uploaded_file(archivos,unidecode(request.session['tienda'].nombre).replace(' ','-'))
					for image in request.FILES.getlist('file'):
						anuncio.imagen='imagenes/tiendas/'+unidecode(request.session['tienda'].nombre).replace(' ','-').replace(' ','-')+'/'+unidecode(unicode(image.name))
						

					anuncio.fecha=datetime.now().strftime("%Y-%m-%d")
					anuncio.activo=1
					anuncio.save()

				except ObjectDoesNotExist:
					anuncio=Anuncios()

					objetcUpdate(anuncio,request.POST)

					archivos=request.FILES.getlist('file')

					handle_uploaded_file(archivos,unidecode(request.session['tienda'].nombre).replace(' ','-'))
					for image in request.FILES.getlist('file'):
						anuncio.imagen='imagenes/tiendas/'+unidecode(request.session['tienda'].nombre).replace(' ','-')+'/'+unidecode(unicode(image.name)).replace(' ','-')


					anuncio.fecha=datetime.now().strftime("%Y-%m-%d")
					anuncio.tipo='A'
					anuncio.activo=1

					anuncio.tienda=request.session['tienda']
					anuncio.save()
				dic['letrero']='Anuncio Agregado'
				getErrorLabel(False,dic)
			except Exception, e:
				print e
				dic['letrero']='Oops! ocurrio un error'
				getErrorLabel(True,dic)

	return render_to_response('AnuncioAdd.html',context_instance=RequestContext(request,dic))

def anunciosList(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])
	tienda=request.session['tienda'];
	anuncios=Anuncios.objects.all().filter(tienda=tienda).filter(activo=1).order_by('-idanuncios')
	dic={'Usuario':cliente.nombre,
	 	 'logo':tienda.logo,
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'pago':request.session['habil'],
	 	 'titulo':'Anuncios',
	 	 'anuncios':anuncios,
	 	 'ver':'none'}

	return render_to_response('anuncios.html',context_instance=RequestContext(request,dic))

def addSendForm(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	tienda=request.session['tienda']
	cliente=getUser(request.session["cliente"])
	metodos=Formaenvio.objects.all().filter(tiendaformaenvio__tienda=tienda).filter(activo__exact=1)



	metodosExtras=Formaenvio.objects.filter(activo__exact=1).exclude(idformaenvio__in=TiendaFormaenvio.objects.filter(tienda=tienda).values_list('formaenvio', flat=True))
	print metodosExtras
	dic={'Usuario':cliente.nombre,
	 	 'logo':tienda.logo,
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'pago':request.session['habil'],
	 	 'titulo':'Envios',
	 	 'ver':'none',
	 	 'metodos':metodos,
	 	 'metodosExtra':metodosExtras
	 	 }

	return render_to_response('enviosAdd.html',context_instance=RequestContext(request,dic))

def addUnit(request):
	dic={'Error':True} 
	if request.is_ajax():
		if request.POST:
			try:
				unidad=Unidades()
				unidad.nombre=request.POST['nombreUnidad']
				unidad.prefijo=request.POST['prefijo']
				unidad.save();
				unidades=Unidades.objects.values()
				dic['Error']=False
				dic['unidades']='<option value="'+request.POST['nombreUnidad']+'" selected="selected">'+request.POST['nombreUnidad']+' ('+request.POST['prefijo']+')</option>'
				return HttpResponse(
					json.dumps(dic),
					content_type='application/json;charset=utf8'
					)
			except Exception, e:
				dic['Error']=True
				return HttpResponse(
					json.dumps(dic),
					content_type='application/json;charset=utf8'
					)

	else:
		raise Http404

def getUser(idcliente):
	return Cliente.objects.get(idclientes=idcliente)

def getErrorLabel(bandera,arreglo):
	if bandera==True:
		arreglo['ver']='block'
		arreglo['icono']='icon-sad'
		arreglo['color']='bgcolor-rojo'
	else:
		arreglo['ver']='block'
		arreglo['icono']='icon-checkmark'
		arreglo['color']='bgcolor-verde'

def prox(request,seccion):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])
	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':seccion,
	 	 'ver':'none'}
	return render_to_response('prox.html',context_instance=RequestContext(request,dic))

def User(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	listaTiendas=[]
	cliente=getUser(request.session["cliente"])
	superCliente=Cliente.objects.get(idclientes__exact=str(cliente.idclientes))
	tiendasCliente=ClientesTiendas.objects.filter(clientes=superCliente,activo=1)
	for t in tiendasCliente:
		listaTiendas.append(t.tiendas)

	tiendas=Tienda.objects.filter(idtienda__in=listaTiendas)
	contratos=Contrato.objects.filter(clientes_idclientes=superCliente)

	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':'Mis datos',
	 	 'cliente':cliente,
	 	 'superCliente':superCliente,
	 	 'tiendas':tiendas,
	 	 'contrato':contratos,
	 	 'ver':'none'}

	return render_to_response('User.html',context_instance=RequestContext(request,dic))

def miTienda(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])
	tienda=request.session['tienda']


	dic={'Usuario':cliente.nombre,
	 	 'logo':tienda.logo,
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'pago':request.session['habil'],
	 	 'titulo':'Mi tienda',
	 	 'tienda':tienda,
	 	 'tiendaDescripcion': stripjs(tienda.descripcion),
	 	 'ver':'none'}

	if request.POST:
		valores=fun.validarForm(request.POST)

		if(valores['vacio']==True):
			dic['letrero']=valores['valores']+' vacio'
			getErrorLabel(True,dic)
		else:
			try:

				objetcUpdate(tienda,request.POST)

				if request.FILES.getlist('logo'):
					archivos=request.FILES.getlist('logo')
					handle_uploaded_file(archivos,unidecode(request.session['tienda'].nombre).replace(' ','-'))
					for image in request.FILES.getlist('logo'):
						tienda.logo='imagenes/tiendas/'+unidecode(request.session['tienda'].nombre).replace(' ','-')+'/'+unidecode(unicode(image.name)).replace(' ','-')


				tienda.save()
				request.session['tienda']=tienda
				dic['logo']=tienda.logo
				dic['letrero']='Cambios Guardados'
				getErrorLabel(False,dic)
			except Exception, e:
				dic['letrero']='Oops! ocurrio un error'
				getErrorLabel(True,dic)

	return render_to_response('tienda.html',context_instance=RequestContext(request,dic))

def Editor(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])
	tienda=request.session['tienda']
	categorias=Categorias.objects.all().filter(stock=request.session['stockAdmin'].idstock)
	productos=Productos.objects.all().extra(select={'nombre':'Productos.Nombre','archivo':'Galeria.Archivo'}).filter(galeria__tipo="A").filter(categorias__in=categorias).filter(activo=1).order_by('-idproductos').filter(activo=1).distinct()[0:8]



	anuncios=Anuncios.objects.all().filter(tienda__exact=tienda).filter(activo__exact=1)


	conjunto=Conjunto.objects.get(tienda__exact=tienda.idtienda)
	secciones=Secciones.objects.all().filter(conjunto__exact=conjunto)
	pie=Secciones.objects.get(conjunto__exact=conjunto,nombre='Pie')
	cabecera=Secciones.objects.get(conjunto__exact=conjunto,nombre='Cabecera')

	if request.POST:
		for n in request.POST:
			for s in seccionesNombre:
				if s in n:
					if request.POST[n] != '':
						try:
							propiedadExistente=Propiedades.objects.get(nombre__exact=n,secciones__exact=pie)
							propiedadExistente.valor=request.POST[n]
							propiedadExistente.save()	
						except:
							propiedad=Propiedades()
							propiedad.nombre=n
							propiedad.valor=request.POST[n]
							propiedad.secciones=pie
							propiedad.save()

		if request.FILES.getlist('imagenFondo'):
			archivos=request.FILES.getlist('imagenFondo')
			handle_uploaded_file(archivos,unidecode(request.session['tienda'].nombre).replace(' ','-'))
			try:
				propiedadExistente=Propiedades.objects.get(nombre__exact='imagenFondo',secciones__exact='Cuerpo')
				propiedadExistente.valor='imagenes/tiendas/'+unidecode(request.session['tienda'].nombre).replace('-','')+'/'+request.FILES.get('logo').name		
				propiedadExistente.save()	
			except:
				propiedad=Propiedades()
				propiedad.nombre='imagenFondo'
				propiedad.valor='imagenes/tiendas/'+unidecode(request.session['tienda'].nombre).replace('-','')+'/'+request.FILES.get('imagenFondo').name
				propiedad.secciones=Secciones.objects.get(conjunto__exact=conjunto,nombre='Cuerpo')
				propiedad.save()


	propiedad=Propiedades.objects.all().filter(secciones__in=secciones)

	datos={'template':1,
		'color':'green',
		'colorNavegador':'black',
		'colorLogo':'red',
		'pie':pie.contenido,
		'cabecera':cabecera.contenido,
		'logo':tienda.logo,
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'pago':request.session['habil'],
		'productos':productos,
		'anuncios':anuncios,
		'categorias':categorias

		}
	propiedad=Propiedades.objects.all().filter(secciones__in=secciones)
	for p in propiedad:
		datos[p.nombre]=p.valor

	datos['sesion']='false'


	return render_to_response('engineEditor.html',context_instance=RequestContext(request,datos))

def paginar(contador):
	paginas=contador/15
	if contador%15!=0:
		paginas=paginas+1
	return paginas

def objetcUpdate(objeto,lista):
	listaObjeto=objeto.__dict__
	for atributo in listaObjeto:
		if atributo in lista:
			if atributo!='logo':
				objeto.__dict__[atributo]=lista[atributo]

def eliminar(request):
	dic={'Error':True}
	itemiterator='' 
	if request.is_ajax():
		if request.POST:
			try:
				""" item=elementos[request.POST['elemento']].objects.get(idproductos__exact=request.POST['idproducto'])
				item.activo=0
				item.save();"""
				if request.POST['elemento']=='PaquetesFormaenvio':

					items=PaquetesFormaenvio.objects.all().extra(where=[" Paquetes = %s and FormaEnvio = %s "],params=[request.POST['iditem'],request.POST['forma']])				
					v=''
					for i in items:
						t=PaquetesFormaenvio.objects.filter(paquetes=i.paquetes).filter(formaenvio=i.formaenvio).filter(zonas=i.zonas).update(activo=0)
					dic={'Error':False} 
				else:

					item=getItem(request.POST['elemento'],request.POST['iditem'])
					item.activo=0
					item.save();
					dic={'Error':False} 
			except Exception, e:
				dic['Error']=True
				return HttpResponse(
					json.dumps(dic),
					content_type='application/json;charset=utf8'
					)


		return HttpResponse(
				json.dumps(dic),
				content_type='application/json;charset=utf8'
				)
	else:
		raise Http404

def getItem(item,iditem):
	elemento=''
	if item=='Productos':
		elemento=Productos.objects.get(idproductos__exact=iditem)
	elif item=='Anuncios':
		elemento=Anuncios.objects.get(idanuncios__exact=iditem)
	elif item=='Clientes':
		elemento=Clientes.objects.get(idclientes__exact=iditem)
	elif item=='Pedidos':
		elemento=Pedidos.objects.get(idpedidos__exact=iditem)
	elif item=='Categorias':
		elemento=Categorias.objects.get(idcategorias__exact=iditem)		
	return elemento

def modifyProduct(request,idproducto):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])
	unidades=Unidades.objects.values()
	categorias=Categorias.objects.all().filter(stock=request.session['stockAdmin'],activo=1)
	producto=Productos.objects.get(idproductos__exact=idproducto)
	request.session["categoria"]=producto.categorias
	existenciasProducto=0
	modelos=Modelos.objects.all().filter(productos__exact=producto).filter(activo__exact=1).exclude(nombre__exact=producto.nombre.encode('utf8'))

	imagenes=Galeria.objects.all().filter(productos__exact=producto).filter(activo__exact=1)

	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':'Agregar Productos',
	 	 'ver':'none',
	 	 'unidades':unidades,
	 	 'categorias':categorias,
	 	 'producto':producto,
	 	 'modelos':modelos,
	 	 'imagenes':imagenes,
	 	 'action':'/producto/'+idproducto+'/'
	 	 }

	listaModelos=[]
	contador=0
	for m in modelos:
		listaModelos.insert(contador, m.nombre) 
		contador=contador+1

	if request.POST:
		valores=fun.validarForm(request.POST)

		if(valores['vacio']==True):
			dic['letrero']=valores['valores']+' vacio'
		else:
			#modelos Existentes
			for l in listaModelos:
				modelo=Modelos.objects.get(nombre__exact=l,productos__exact=producto)
				key=request.POST.get('nombreModeloExistente_'+l,False)

				if not key:
					modelo.activo=0
					modelo.save()
				else:
					modelo.nombre=request.POST['nombreModeloExistente_'+l]
					modelo.nombre=request.POST['nombreModeloExistente_'+l]
					modelo.precio=request.POST['precioModeloExistente_'+l]
					modelo.descripcion=request.POST['descripcionModeloExistente_'+l]
					modelo.existencias=request.POST['existenciasModeloExistente_'+l]
					modelo.save()
					existenciasProducto=existenciasProducto+float(modelo.existencias)
			#Modelos Nuevos
			for e in request.POST:
				if 'nombreModelo_' in str(e): 	
					test=e
					test=test.replace('nombreModelo_','')	
					try:
						#verifico si el modelo ya existia

						modeloNuevo=Modelos.objects.get(nombre=request.POST['nombreModelo_'+test],productos=producto)
						modeloNuevo.precio=request.POST['precioModelo_'+test]
						modeloNuevo.descripcion=request.POST['descripcionModelo_'+test]
						modeloNuevo.productos=producto
						modeloNuevo.existencias=request.POST['existenciasModelo_'+test]
						modeloNuevo.activo=1
						modeloNuevo.save()
						existenciasProducto=existenciasProducto+int(modeloNuevo.existencias)

					except ObjectDoesNotExist:	
						#si el modelo no existe lo crea
						modeloNuevo=Modelos()
						modeloNuevo.nombre=request.POST['nombreModelo_'+test]
						modeloNuevo.precio=request.POST['precioModelo_'+test]
						modeloNuevo.descripcion=request.POST['descripcionModelo_'+test]
						modeloNuevo.existencias=request.POST['existenciasModelo_'+test]
						modeloNuevo.productos=producto
						modeloNuevo.activo=1
						modeloNuevo.save()
						existenciasProducto=existenciasProducto+int(modeloNuevo.existencias)


			#modelo origen del producto se actualiza el nombre
			modelo=Modelos.objects.get(nombre__exact=producto.nombre.encode('utf8'),productos=producto)
			modelo.nombre=request.POST['nombre']
			if existenciasProducto > 0:
				modelo.existencias=existenciasProducto
			else:
				modelo.existencias=request.POST['existencias']
			modelo.save()

			categoria=Categorias.objects.get(nombre__exact=request.POST['categoria'],stock=request.session['stockAdmin'])
			unidad=Unidades.objects.get(nombre=request.POST['unidad'])
			objetcUpdate(producto,request.POST)
			producto.categorias=categoria
			producto.unidad=unidad
			producto.activo=1
			producto.save()





			modelos=Modelos.objects.all().filter(productos__exact=producto).filter(activo__exact=1).exclude(nombre__exact=producto.nombre.encode('utf8'))
			dic['modelos']=modelos
			dic['modelo']=modelo

			if request.FILES.getlist('files[]'):
				for i in imagenes:
					try:
						os.unlink(os.path.join(settings.STATIC_URL, i.archivo))
					except Exception, e:
						print "error " + e.message
					i.delete()

				archivos=request.FILES.getlist('files[]')

				handle_uploaded_file(archivos,unidecode(request.session['tienda'].nombre).replace(' ','-'))

				contador=0
				for image in request.FILES.getlist('files[]'):
					if contador<=3:
						imagen=Galeria()
						imagen.nombre=image.name
						imagen.archivo='imagenes/tiendas/'+unidecode(unicode(request.session['tienda'].nombre)).replace(' ','-')+'/'+unidecode(unicode(image.name)).replace(' ','-')


						print imagen.archivo
						if contador==0:
							imagen.tipo='A'
						else:
							imagen.tipo='B'
						imagen.activo=1
						imagen.productos=producto
						imagen.save()
						contador=contador+1

			imagenes=Galeria.objects.all().filter(productos__exact=producto).filter(activo__exact=1)
			dic['imagenes']=imagenes
			dic['letrero']='Cambios Guardados'
			getErrorLabel(False,dic)

		
	return render_to_response('productosAdd.html',context_instance=RequestContext(request,dic))

def addMetodo(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])
	tienda=request.session['tienda']

	dic={'Usuario':cliente.nombre,
	 	 'logo':tienda.logo,
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'pago':request.session['habil'],
	 	 'titulo':'Agregar Método',
	 	 'ver':'none'
	 	 }
	if request.POST:
		valores=fun.validarForm(request.POST)

		if(valores['vacio']==True):
			dic['letrero']=valores['valores']+' vacio'
		else:
			try:
				try:
					Formaenvio.objects.get(nombre=request.POST['nombre'])

				except ObjectDoesNotExist:	
					metodo=Formaenvio()

					objetcUpdate(metodo,request.POST)

					if request.FILES.getlist('logo'):
						archivos=request.FILES.getlist('logo')
						handle_uploaded_file(archivos,tienda.nombre)

						metodo.logo='imagenes/tiendas/'+str(tienda.nombre).replace(' ','-').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n')+'/'+str(request.FILES.get('logo').name).replace(' ','-').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n')

					metodo.activo=1

					metodo.save()
					tf=TiendaFormaenvio()
					tf.tienda=tienda
					tf.formaenvio=metodo
					tf.activo=1
					tf.save()

				dic['letrero']='Método Agregado'
				getErrorLabel(False,dic)
			except Exception, e:
				dic['letrero']='Oops! ocurrio un error' +e 
				getErrorLabel(True,dic)

	return render_to_response('metodosAdd.html',context_instance=RequestContext(request,dic))
 
def addMetodoE(request):
	dic={}
	if request.is_ajax():
		if request.POST:
			tienda=request.session['tienda']
			print request.POST['forma']
			metodo=Formaenvio.objects.get(idformaenvio__exact=int(request.POST['forma']))
			"""tf=TiendaFormaenvio()
			tf.tienda=tienda
			tf.formaenvio=metodo
			tf.activo=1
			tf.save()"""
			link = connection.cursor()
			query='Insert into Tienda_Formaenvio values('+str(tienda.idtienda)+','+str(metodo.idformaenvio)+',1)'
			link.execute(query)
			link.close()
			dic['Error']=False
			try:
			    transaction.commit_unless_managed()
			except DatabaseError, IntegrityError:
			    getErrorLabel(True,dic)




		return HttpResponse(
						json.dumps(dic),
						content_type='application/json;charset=utf8'
						)
	else:
		raise Http404

def paquetes(request,metodo):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])
	tienda=request.session['tienda']
	forma=Formaenvio.objects.get(idformaenvio__exact=metodo)
	paquetes=Paquetes.objects.all().filter(tienda=tienda).filter(paquetesformaenvio__formaenvio__exact=forma,paquetesformaenvio__activo=1).filter().filter(activo=1).distinct().order_by('-idpaquetes')


	dic={'Usuario':cliente.nombre,
	 	 'logo':tienda.logo,
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'pago':request.session['habil'],
	 	 'titulo':'Paquetes ',
	 	 'paquetes':paquetes,
	 	 'ver':'none',
	 	 'metodo':metodo,
	 	 'forma':forma.idformaenvio
	 	 }

	return render_to_response('paquetes.html',context_instance=RequestContext(request,dic))

def paquetesAdd(request,metodo):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	conector = connection.cursor()
	bandera=False
	cliente=getUser(request.session["cliente"])
	tienda=request.session['tienda']
	paquetesTiendas=Paquetes.objects.all().filter(tienda=tienda).filter(activo=1).filter(paquetesformaenvio__activo=1,paquetescategorias__activo=1)

	categoriasUsadas=Categorias.objects.all().filter(paquetescategorias__paquetes__in=paquetesTiendas,paquetescategorias__activo=1).extra(where=['Categorias.Activo=1'])

	categorias=Categorias.objects.all().filter(stock=request.session['stockAdmin'],activo=1).exclude(idcategorias__in=categoriasUsadas)

	zonas=Zonas.objects.all().filter(tienda__exact=tienda)
	forma=Formaenvio.objects.get(idformaenvio__exact=metodo)

	paquetes=Paquetes.objects.all().filter(tienda=tienda).filter(activo=1).distinct().order_by('-idpaquetes')

	try:
	    transaction.commit_unless_managed()
	except DatabaseError, IntegrityError:
	    getErrorLabel(True,dic)

	#paquetes=Paquetes.objects.all().filter(tienda=tienda).exclude(paquetesformaenvio__formaenvio__exact=forma).filter(activo=1).distinct().order_by('-idpaquetes')


	dic={'Usuario':cliente.nombre,
	 	 'logo':tienda.logo,
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'pago':request.session['habil'],
	 	 'titulo':'Agregar Paquete',
	 	 'zonas':zonas,
	 	 'ver':'none',
	 	 'metodo':metodo,
	 	 'paquetes':paquetes,
	 	 'categorias':categorias
	 	 }

	if not categorias.count()>0:
		dic['nota']='Agregar Nueva Categoria'
	dic['nota']=str(paquetes)

	if request.POST:
		test=''
		test2=''
		paquete={}
		try:
			if request.POST.get('categorias[]',False):
				paquete=Paquetes();
				objetcUpdate(paquete,request.POST)
				paquete.tienda=tienda
				paquete.activo=1
				paquete.save()
			else:
				paquete=Paquetes.objects.get(nombre__exact=request.POST['nombre'],tienda__exact=tienda)

			for e in request.POST:
				if 'zona_' in str(e): 	
					test=e
					test=test.replace('zona_','')
					zona=Zonas.objects.get(idzonas__exact=request.POST[e])

					try:
						conector.execute("Insert Into Paquetes_Formaenvio (Paquetes,FormaEnvio,Zonas,Activo,Importe) values('"+str(paquete.idpaquetes)+"','"+str(forma.idformaenvio)+"','"+str(zona.idzonas)+"','1','"+str(request.POST['precio_'+test])+"')")
						try:
						    transaction.commit_unless_managed()
						except DatabaseError, IntegrityError:
						    getErrorLabel(True,dic)
					except Exception, pe:


						conector.execute('Update Paquetes_Formaenvio set Activo=1,Importe='+str(request.POST['precio_'+test])+' where Paquetes='+str(paquete.idpaquetes)+' and Zonas='+str(zona.idzonas)+' and FormaEnvio='+str(forma.idformaenvio))
						try:
						    transaction.commit_unless_managed()
						except DatabaseError, IntegrityError:
						    getErrorLabel(True,dic)



			if request.POST.get('categorias[]',False):
				for c in request.POST.getlist('categorias[]'):
					categoria=Categorias.objects.get(idcategorias__exact=c)

					conector.execute('Insert Into Paquetes_Categorias values('+str(paquete.idpaquetes)+','+str(categoria.idcategorias)+',1)')
					#conector.execute('Insert Into Paquetes_Categorias values(1,2,1)')
					try:
					    transaction.commit_unless_managed()
					except DatabaseError, IntegrityError:
					    getErrorLabel(True,dic)
					"""pc=PaquetesCategorias()
					pc.paquetes=paquete
					test2=c
					pc.activo=1
					pc.categorias=Categorias.objects.get(idcategorias__exact=c)
					pc.save()"""

			dic['letrero']='Método Agregado'
			getErrorLabel(False,dic)
		except Exception, e:
			dic['letrero']='Oops! ocurrio un error'
			getErrorLabel(True,dic)



		getErrorLabel(False,dic)	
		conector.close()


	return render_to_response('paquetesAdd.html',context_instance=RequestContext(request,dic))

def paquetesModify(request,metodo,pack):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	bandera=False
	conector = connection.cursor()
	cliente=getUser(request.session["cliente"])
	tienda=request.session['tienda']
	paquete=Paquetes.objects.get(idpaquetes=pack)

	paquetesTiendas=Paquetes.objects.all().filter(tienda=tienda).filter(activo=1).filter(paquetesformaenvio__activo=1,paquetescategorias__activo=1).exclude(idpaquetes=pack)


	for p in paquetesTiendas:
		print p.idpaquetes

	categoriasUsadas=Categorias.objects.all().filter(paquetescategorias__paquetes__in=paquetesTiendas,paquetescategorias__activo=1).extra(where=['Categorias.Activo=1'])

	print categoriasUsadas

	categorias=Categorias.objects.all().filter(stock=request.session['stockAdmin'],activo=1).exclude(idcategorias__in=categoriasUsadas)


	zonasT=Zonas.objects.all().filter(tienda__exact=tienda)
	zonas=Zonas.objects.raw('SELECT Zonas.idZonas,Zonas.idZonas as Id, Zonas.Nombre as Nombre,Paquetes_Formaenvio.Importe as precio FROM Zonas inner join Paquetes_Formaenvio on Zonas.idZonas= Paquetes_Formaenvio.Zonas where Paquetes_Formaenvio.formaenvio='+metodo+' and Paquetes_Formaenvio.Activo=1 and Paquetes_Formaenvio.paquetes='+pack)

	forma=Formaenvio.objects.get(idformaenvio__exact=metodo)
	categoriasE=Categorias.objects.all().filter(paquetescategorias__paquetes=pack,paquetescategorias__activo=1)


	lista=[]
	listaids=[]
	listazonas=[]
	listazonasids=[]
	for c in categoriasE:
		lista.append(str(c.slug))
		listaids.append(str(c.idcategorias))

	for z in zonas:
		listazonas.append(str(z.nombre))
		listazonasids.append(int(z.pk))

	dic={'Usuario':cliente.nombre,
	 	 'logo':tienda.logo,
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'pago':request.session['habil'],
	 	 'titulo':'Agregar Paquete',
	 	 'zonas':zonas,
	 	 'zonasT':zonasT,
	 	 'ver':'none',
	 	 'metodo':metodo,
	 	 'p':paquete,
	 	 'categorias':categorias,
	 	 'categoriasE':lista
	 	 }
	try:
		if request.POST:
			test=''
			test2=''
			objetcUpdate(paquete,request.POST)
			paquete.save()

			for e in request.POST:
				if 'zona_' in str(e):
					test=e
					test=test.replace('zona_','')


					try: 	
						"""pfe=PaquetesFormaenvio()
						pfe.paquetes=paquete
						pfe.formaenvio=forma
						pfe.activo=1
						pfe.zonas=Zonas.objects.get(idzonas__exact=request.POST[e])
						pfe.importe=request.POST['precio_'+test]
						pfe.save()"""
						zona=Zonas.objects.get(idzonas__exact=request.POST[e])

						conector.execute('Insert into Paquetes_Formaenvio values('+str(paquete.idpaquetes)+','+str(forma.idformaenvio)+','+str(zona.idzonas)+',1,'+request.POST['precio_'+test]+')')


						try:
						    transaction.commit_unless_managed()
						except DatabaseError, IntegrityError:
						    getErrorLabel(True,dic)
					except Exception, es:
						precio=request.POST['precio_'+test]
						conector.execute("Update Paquetes_Formaenvio set Activo=1, Importe="+precio+" where Zonas="+request.POST[e]+" and Paquetes="+str(paquete.idpaquetes)+" and FormaEnvio="+metodo)


				elif 'zonaE_' in str(e):
					test=e
					test=test.replace('zonaE_','')
					pfe=PaquetesFormaenvio.objects.filter(paquetes=paquete).filter(zonas=test).filter(formaenvio=forma).update(importe=request.POST['precioE_'+test])
					test=int(test)
					listazonasids.remove(test)

			for z in listazonasids:
				PaquetesFormaenvio.objects.filter(paquetes=paquete).filter(zonas=z).filter(formaenvio=forma).update(activo=0)



			link = connection.cursor()
			for c in request.POST.getlist('categorias[]'):
				print str(listaids)
				if c not in listaids:
					try:

						categoria=Categorias.objects.get(idcategorias__exact=c)

						conector.execute('Insert Into Paquetes_Categorias values('+str(paquete.idpaquetes)+','+str(categoria.idcategorias)+',1)')
						#conector.execute('Insert Into Paquetes_Categorias values(1,2,1)')
						try:
						    transaction.commit_unless_managed()
						except DatabaseError, IntegrityError:
						    getErrorLabel(True,dic)
					except Exception, e:
						categoria=Categorias.objects.get(idcategorias__exact=c)

						conector.execute('Update Paquetes_Categorias  set Activo=1 where Paquetes='+str(paquete.idpaquetes)+' and Categorias='+str(categoria.idcategorias))
						#conector.execute('Insert Into Paquetes_Categorias values(1,2,1)')
						try:
						    transaction.commit_unless_managed()
						except DatabaseError, IntegrityError:
						    getErrorLabel(True,dic)

						"""pc=PaquetesCategorias()
						pc.paquetes=paquete
						pc.categorias=Categorias.objects.get(idcategorias__exact=c)
						pc.activo=1
						pc.save()"""



				else:
					 listaids.remove(c)

			for c in listaids:
				PaquetesCategorias.objects.filter(paquetes__exact=paquete).filter(categorias__exact=c).update(activo=0)

			categoriasE=Categorias.objects.all().filter(paquetescategorias__paquetes=pack,paquetescategorias__activo=1)
			paquete=Paquetes.objects.get(idpaquetes=pack)
			lista=[]
			for c in categoriasE:
				lista.append(str(c.slug))
			dic['categoriasE']=lista

			dic['letrero']='Cambios Guardados'
			getErrorLabel(False,dic)	
			conector.close()
	except Exception, e:
		dic['letrero']='Oops! ocurrio un error'
		getErrorLabel(True,dic)

	return render_to_response('paquetesModify.html',context_instance=RequestContext(request,dic))

def addZone(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	dic={'Error':True} 
	listaEstados='';
	if request.is_ajax():
		if request.POST:
			try:
				for e in request.POST.getlist('estados[]'):
					listaEstados+=e+','

				tienda=request.session['tienda']
				zona=Zonas()
				zona.nombre=request.POST['nombre']
				zona.descripcion=request.POST['descripcion']
				zona.tienda=tienda
				zona.estados=listaEstados
				zona.activo=1
				zona.save()
				zonas=Zonas.objects.all().filter(tienda__exact=tienda)
				listaZonas=''
				for z in zonas:
					listaZonas+=z.estados+','

				dic['Error']=False
				dic['zona']=request.POST['nombre']
				dic['idzona']=zona.idzonas
				dic['zonas']=listaZonas
				return HttpResponse(
					json.dumps(dic),
					content_type='application/json;charset=utf8'
					)

			except Exception, e:
				dic['Error']=True
				return HttpResponse(
					json.dumps(dic),
					content_type='application/json;charset=utf8'
					)

	else:
		raise Http404

def pasarelas(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')


	cliente=getUser(request.session["cliente"])
	tienda=request.session['tienda']
	listaMetodos=[]

	dic={'Usuario':cliente.nombre,
	 	 'logo':tienda.logo,
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'pago':request.session['habil'],
	 	 'titulo':'Pagos ONLINE',
	 	 'ver':'none'

	 	 }



	if request.session['habil'] == '':

		metodos=Formapago.objects.all().exclude(nombre__exact='Conekta')


		metodosE=TiendaFormapago.objects.raw("Select * from Tienda_Formapago where Tienda="+str(tienda.idtienda)+" and FormaPago!='Conekta' and Activo=1")

		for m in metodosE:
			listaMetodos.append(str(m.formapago))

		if request.POST:
			valores=fun.validarForm(request.POST)

			if(valores['vacio']==True):
				dic['letrero']=valores['valores']+' vacio'
			else:
				try:
					metodo=TiendaFormapago.objects.get(tienda=tienda,formapago='Conekta')
				
					TiendaFormapago.objects.filter(tienda=tienda).update(llaveprivada=request.POST['privada'],llavepublica=request.POST['publica'])


				except ObjectDoesNotExist:
					link = connection.cursor()
					"""tf=TiendaFormapago()
					tf.tienda=tienda
					tf.formapago=Formapago.objects.get(nombre='Conekta')
					tf.llaveprivada=request.POST['privada']
					tf.llavepublica=request.POST['publica']
					tf.activo=1
					tf.save()"""
					forma=Formapago.objects.get(nombre='Conekta')
					query='Insert into Tienda_Formapago values('+str(tienda.idtienda)+',"'+forma.nombre+'","'+request.POST['privada']+'","'+request.POST['publica']+'",1)'
					link.execute(query)
					link.close()

					try:
						transaction.commit_unless_managed()
					except DatabaseError, IntegrityError:
						getErrorLabel(True,dic)

				for m in request.POST.getlist('metodos[]'):
					if not m in listaMetodos:
						try:
							tfp=TiendaFormapago.objects.get(formapago=m,tienda=tienda)
							tfp.activo=1
							tfp.save()
						except ObjectDoesNotExist:

							tfp=TiendaFormapago()
							tfp.formapago=Formapago.objects.get(nombre=m)
							tfp.tienda=tienda
							tfp.activo=1
							tfp.llaveprivada=request.POST['privada']
							tfp.llavepublica=request.POST['publica']
							tfp.save()
							try:
								transaction.commit_unless_managed()
							except DatabaseError, IntegrityError:
								getErrorLabel(True,dic)
					else:
						listaMetodos.remove(m)

				for m in listaMetodos:
					tfp=TiendaFormapago.objects.get(formapago=m,tienda=tienda)

					tfp.activo=0
					tfp.save()

				listaMetodos=[]		

				metodosE=TiendaFormapago.objects.raw("Select * from Tienda_Formapago where Tienda="+str(tienda.idtienda)+" and  FormaPago!='Conekta' and Activo=1")

				for m in metodosE:
					listaMetodos.append(str(m.formapago))

				dic['letrero']='Cambios Guardados'
				getErrorLabel(False,dic)

				dic['ver']='show'



		pasarelas=TiendaFormapago.objects.all().filter(tienda=tienda)
		contador=pasarelas.count()
		pasarelaE={}
		pasarela=Formapago.objects.get(nombre__exact='Conekta')

		pE=TiendaFormapago.objects.raw("Select * from Tienda_Formapago where Tienda="+str(tienda.idtienda)+" and FormaPago='Conekta'")
		for p in pE:
			pasarelaE=p

		dic['pasarelas']=pasarelas
		dic['pasarela']=pasarela
		dic['contador']=contador
		dic['pasarelaE']=pasarelaE
		dic['metodos']=metodos
		dic['metodosE']=listaMetodos
	else:
		dic['Error']='Activa Tu Tienda'


	return render_to_response('pasarelas.html',context_instance=RequestContext(request,dic))

def clientesTienda(request):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')
	cliente=getUser(request.session["cliente"])

	stock=Stock.objects.get(tienda__exact=request.session['tienda'])
	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':'Mis Clientes',
	 	 'ver':'none'}

	clientes=Clientes.objects.all().filter(tienda=request.session['tienda'],activo=1).select_related('tipocliente__stock').extra(select={'tipo':'TipoCliente.Nombre'}).order_by('idclientes')



	paginator = Paginator(clientes,15)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
	try:
		fp = paginator.page(page)
	except (EmptyPage, InvalidPage):
		fp = paginator.page(paginator.num_pages)

	dic['clientes']=fp

	return render_to_response('clientesTienda.html',context_instance=RequestContext(request,dic))

def detallePedido(request,id):
	if not validarUser(request):
		return HttpResponseRedirect('/ingresar/True/')

	cliente=getUser(request.session["cliente"])

	stock=Stock.objects.get(tienda__exact=request.session['tienda'])
	dic={'Usuario':cliente.nombre,
	 	 'logo':request.session['tienda'].logo,
	 	 'pago':request.session['habil'],
	 	 'miPagina':Site.objects.get(id=request.session['tienda'].site_id),
	 	 'titulo':'Detalle Pedido',
	 	 'ver':'none',}
	try:
		pedido=Pedidos.objects.get(idpedidos=id, stock=stock,activo=1)
		dic['pedido']=pedido
		dic['Error']=False
		cargo=Cargos.objects.get(pedidos=pedido)
		dic['cargo']=cargo
		productos=PedidosProductos.objects.all().filter(pedidos=pedido)
		dic['productos']=productos
		dic['total']=str(float(pedido.importe)+float(pedido.importeenvio))
	except ObjectDoesNotExist:
		dic['Error']=True
		dic['errorLetrero']='No se encontro el pedido'

	clientes=Clientes.objects.filter(tienda=request.session['tienda']).filter(tipocliente__stock_idstock__exact=stock)

	return render_to_response('pedido.html',context_instance=RequestContext(request,dic))

def eventCompletar(request):
	event_json = json.loads(HttpRequest.body)
	print event_json


def Completar(request):
	dic={'Error':True} 
	if request.is_ajax():
		if request.POST:
			try:
				pedido=Pedidos.objects.get(idpedidos=request.POST['idpedido'])
				pedido.status='Completado'
				pedido.save()
				dic['Error']=False
				return HttpResponse(
					json.dumps(dic),
					content_type='application/json;charset=utf8'
					)
			except Exception, e:
				dic['Error']=True
				return HttpResponse(
					json.dumps(dic),
					content_type='application/json;charset=utf8'
					)

	else:
		raise Http404

def validarUser(request):
	if request.session.get('user',False):
		if request.session["user"]==False:
			return False
		else:
			return True
	else:
		return False


def salir(request):
	request.session["user"]=False
	return HttpResponseRedirect('/')


@csrf_exempt
def Confirmar(request):
	try:
		event_json = json.loads(str(request.body))

		data= event_json['data']
		data1=data['object']
		status=data1['status']
		idCargo=data1['id']
		
		if status == 'paid':
			try:

				cargo=Cargos.objects.get(idcargo=str(idCargo))
				print idCargo
				cargo.status='A'
				cargo.save()


				pedido=Pedidos.objects.get(idpedidos=int(cargo.pedidos.idpedidos))
				pedido.status='Pagado'
				pedido.save()
			except ObjectDoesNotExist:
				print ('el cargo no existe')

	except Exception, e:
		print e
	return HttpResponse(status=200)

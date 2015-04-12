# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from models import *
from cms.models import *
from django.core.mail import *
from storeapp.funciones import Funciones
import urllib2 
import json
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.db import connection
import json
from decimal import *
from django.core.paginator import *
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.exceptions import *
from django.db import transaction,IntegrityError
import datetime
import urllib

import StringIO

#urls amigables
from django.template.defaultfilters import slugify

# identificar el dominio
from django.conf import settings
from django.contrib.sites.models import Site






cursor = connection.cursor()
fun=Funciones()

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





def Correo(request):
    dic={}
    if request.is_ajax():
        if request.POST:
            try:
                tienda=Tienda.objects.get(site_id=settings.SITE_ID)
                
                params2 = {
                        'asunto':'Comentario',
                        'mailreceptor':tienda.mail,
                        'mailemisor':request.POST['mail'],
                        'texto':'<h2>'+request.POST['Nombre']+'</h2><p>'+request.POST['comentario']+'</p>',
                        }

                setMensaje(params2)

                dic['Error']='false'

            except Exception, e:
                raise e
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

def setPass(request):
    datos={}
    getDatos(datos,request)
    tienda=datos['tienda']
    cliente=request.session['idcliente']
    import uuid
    cliente.password=str(uuid.uuid4().hex)[:6]

    cliente.save()

    parametros={
                'mailreceptor':cliente.mail,
                'mailemisor':tienda.mail,
                'asunto':'Tu nuevo password para '+str(tienda.nombre.encode('utf-8')),
                'texto':'<h1>'+str(tienda.nombre.encode('utf-8'))+'</h1>Tu nuevo password es <strong>'+cliente.password+'</strong>',
                }

    print parametros

    setMensaje(parametros)

    return render_to_response('plantilla1/confirmacion.html',context_instance=RequestContext(request,datos))


def login(request):
    datos={'Usuario':'Invalido'}
    if request.POST:
        contador=Administrador.objects.filter(login__exact=request.POST['Nombre'])  
         
        if contador.count()>0:
            m = Administrador.objects.get(login__exact=request.POST['Nombre'])
            if m.pass_field == request.POST['Contrasena']:
                datos={'Usuario':'valido'}

    return HttpResponseRedirect(reverse('login'))   

def loginCliente(request):
    dic={}
    tienda=Tienda.objects.get(site_id=settings.SITE_ID)
    #tienda=Tienda.objects.get(nombre='google.com')
    if request.is_ajax():
        if request.POST:
            valores=fun.validarForm(request.POST)
            if(valores['vacio']==True):
                dic['letrero']=valores['valores']+' vacio'
            else:
                request.session['clienteTienda']=validarCliente(request.POST['user'],request.POST['pass'],tienda)
                if request.session['clienteTienda']==True:
                    dic['Error']=False
                    request.session['idcliente']=Clientes.objects.get(mail=request.POST['user'],password=request.POST['pass'],tienda=tienda)
                else:
                    dic['Error']=True
        return HttpResponse(
                        json.dumps(dic),
                        content_type='application/json;charset=utf8')           
                    
    else:
        raise Http404

def registroClientes(request):
    dic={}
    if request.is_ajax():
        if request.POST:
            valores=fun.validarForm(request.POST)
            if(valores['vacio']==True):
                dic['letrero']=valores['valores']+' vacio'
            else:
                try:
                    Clientes.objects.get(mail=request.POST['mail'],tienda=Tienda.objects.get(site_id=settings.SITE_ID))
                    
                    dic['letrero']='El correo ya se encuentra registrado'
                    dic['Error']=True
                except ObjectDoesNotExist:
                    cliente= Clientes()
                    objetcUpdate(cliente,request.POST)
                    import uuid
                    tienda=request.session['tienda']
                    cliente.password    = str(uuid.uuid4().hex)[:6]
                    cliente.activo      = 1
                    cliente.tienda      = request.session['tienda']
                    cliente.tipocliente = Tipocliente.objects.get(idtipocliente=2)
                    cliente.save()
                    parametros          = {
                                            'mailreceptor':str(request.POST['mail']),
                                            'mailemisor':cliente.mail,
                                            'asunto':'Tu password para '+str(tienda.nombre.encode('utf-8')),
                                            'texto':'<h1>'+str(tienda.nombre.encode('utf-8'))+'</h1>Tu nuevo password es '+cliente.password,
                                            }

                    setMensaje(parametros)

                    dic['Error']=False
                    #request.session['clienteTienda']=True
                    #request.session['idcliente']=cliente
        
                return HttpResponse(
                        json.dumps(dic),
                        content_type='application/json;charset=utf8')   

    else:
        raise Http404

def home(request):
    #del request.session['modelos']
    datos={}
    getDatos(datos,request)
    productos=Productos.objects.all().extra(select={'nombre':'Productos.Nombre','archivo':'Galeria.Archivo'}).filter(galeria__tipo="A").filter(categorias__in=datos['categorias']).filter(activo=1).order_by('-idproductos').filter(activo=1).distinct()[0:8]
    #productos=Productos.objects.all()
    anuncios=Anuncios.objects.all().filter(tienda__exact=datos['tienda']).filter(activo__exact=1)
    current_site = Site.objects.get_current()

    datos['productos']=productos
    datos['anuncios']=anuncios

    return render_to_response('plantilla1/index.html',context_instance=RequestContext(request,datos))

def panelUser(request):
    if not validarUser(request):
        return HttpResponseRedirect('/tienda/')

    datos={}


    getDatos(datos,request)

    cliente=request.session['idcliente']
    from django.db.models import Q
    pedidos=Pedidos.objects.filter(activo=1,clientes=cliente,stock=datos['stock']).filter(Q(status='Pendiente') | Q(status='Pagado'))
    datos['titulo']='Bienvenido '+str(cliente.nombre)
    datos['pedidos']=pedidos
    datos['cliente']=cliente



    return render_to_response('plantilla1/panel.html',context_instance=RequestContext(request,datos))


def articulo(request,productoR):
    datos={}
    getDatos(datos,request)
    producto=Productos.objects.filter(galeria__tipo='A').filter(idproductos__exact=productoR).extra(select={'nombre':'Productos.Nombre','archivo':'Galeria.Archivo'})

    imagenes=Galeria.objects.all().filter(productos__exact=producto,tipo='B').filter(activo__exact=1)

    p={}
    for pr in producto:
        p=pr 

    productos=Productos.objects.all().extra(select={'nombre':'Productos.Nombre','archivo':'Galeria.Archivo'}).filter(galeria__tipo="A").filter(categorias=p.categorias).filter(activo=1).exclude(idproductos=p.idproductos).order_by('-idproductos').filter(activo=1).distinct()[0:2]

   
    modelos=Modelos.objects.all().filter(productos__exact=p.idproductos).filter(activo__exact=1).exclude(nombre=p.nombre)

    #verifico cesta y stock de los productos
    stockPrincipal=0

    
    if not modelos.count()>0:
        modelo=Modelos.objects.get(productos=str(p.idproductos),activo__exact=1,nombre=p.nombre)
        datos['modeloProducto']=str(p.idproductos)+':'+str(modelo.idmodelos)
        stockPrincipal=modelo.existencias-getCesta(request,str(modelo.idmodelos))


    else:
        datos['modeloProducto']=modelos.count()
        for m in modelos:
            m.stock=int(m.existencias)-getCesta(request,str(m.idmodelos))
            stockPrincipal=stockPrincipal+m.stock


    datos['producto']=p
    datos['stock']=stockPrincipal
    datos['modelos']=modelos
    datos['imagenes']=imagenes
    datos['productos']=productos
    datos['descripcionTienda']=p.descripcion
    datos['Titulo']=p.nombre



    return render_to_response('plantilla1/detalle.html',context_instance=RequestContext(request,datos))

def setCarrito(request):
    dic={}
    cantidad=0;
    if request.is_ajax():
        if request.POST:
            valores=fun.validarForm(request.POST)
            if(valores['vacio']==True):
                dic['letrero']=valores['valores']+' vacio'
            else:
                existencias=0
                if request.session.get('modelos', False):
                    modelos=request.session['modelos']
                else:
                    request.session['modelos']={}
                    modelos={}

                pro=str(request.POST['modelo'])
                pro=pro.split(':')
                try:
                    producto    = Productos.objects.get(idproductos=pro[0])
                    modelo      = Modelos.objects.get(idmodelos=pro[1])
                    cantidad    = getCesta(request,pro[1])
                    cantidadCesta=0
                    #se verifica si el producto existe en la cesta y se le asigna el valor
                    if modelos.get(request.POST['modelo'],False):
                        cantidadCesta=int(modelos[request.POST['modelo']])
                   
                    #se valida si las existencias son mayores a la cantidad que se intenta introducir
                    if (int(modelo.existencias)-cantidad) >= int(request.POST['cantidad']):

                        dic['Error']=False
                        #se guardan la cantidad en el modelo para despues asignar el modelo en la sesion del carrito
                        modelos[request.POST['modelo']]=cantidadCesta+int(request.POST['cantidad'])
                        request.session['modelos']=modelos
                        dic['cesta']=getTotalCesta(request)

                    else:
                        dic['Error']=True
                        dic['test']='Existencias Insuficientes'

                except ObjectDoesNotExist:
                    dic['Error']=True
                    dic['test']='No se encontro el objeto'
        
        return HttpResponse(
                        json.dumps(dic),
                        content_type='application/json;charset=utf8')           
                    
    else:
        raise Http404

def Carrito(request):
    datos={}
    items={}
    getDatos(datos,request)
    try:
        modelos=request.session['modelos']
        test=''
        total=0
        for p in modelos:
            pro=str(p)
            pro=pro.split(':')
            prod=pro[0]
            modelo=pro[1]
            producto=Productos.objects.get(idproductos=prod)
            modelo=Modelos.objects.get(idmodelos=modelo)
            imagen=Galeria.objects.get(productos=producto,tipo='A')
            precio=(producto.precio*modelos[p])+(modelo.precio*modelos[p])
            total+=precio
            test+=producto.nombre.encode('utf8')+','
            items[producto.nombre.encode('utf8')+modelo.nombre.encode('utf8')]={
                                            'nombre':producto.nombre,
                                            'imagen':imagen.archivo,
                                            'cantidad':modelos[p],
                                            'precioUnitario':producto.precio,
                                            'importe':precio,                                       
                                            'precioModelo':modelo.precio,
                                            'idmodelo':str(producto.idproductos)+":"+str(modelo.idmodelos),
                                            'modelo':modelo.nombre.encode('utf8')
                                        }
        datos['productos']=items
        datos['total']=total

        request.session['total']=total

    except Exception, e:
        datos['letrero']='Oops! ocurrio un error..., Intentalo más tarde '
        request.session["productos"]={}
        request.session["modelos"]={}


    return render_to_response('plantilla1/carrito.html',context_instance=RequestContext(request,datos))

def Procesar(request):
    if not validarUser(request):
        return HttpResponseRedirect('/tienda/')

    datos={}
    if request.POST:
        request.session['comentario']=request.POST['comentario']

    modelos=request.session['modelos']

    test=''
    total=0
    for p in modelos:
        pro=str(p)
        pro=pro.split(':')
        prod=pro[0]
        modelo=pro[1]
        producto=Productos.objects.get(idproductos=prod)
        modelo=Modelos.objects.get(idmodelos=modelo)
        imagen=Galeria.objects.get(productos=producto,tipo='A')
        precio=(producto.precio*modelos[p])+(modelo.precio*modelos[p])
        total+=precio
    

    request.session['precio']   = total
    datos['precio']             = request.session['precio']   
    getDatos(datos,request)
    tienda                      = datos['tienda']
    metodos                     = TiendaFormapago.objects.raw("Select * from Tienda_Formapago where Tienda="+str(tienda.idtienda)+"  and Activo=1")
    datos['metodos']            = metodos
    cliente                     = request.session['idcliente']
    datos['cliente']            = cliente
    llaves                      = TiendaFormapago.objects.get(tienda=Tienda.objects.get(site_id=settings.SITE_ID),formapago__exact='Conekta')

    datos['llave']=llaves.llavepublica

    return render_to_response('plantilla1/procesar.html',context_instance=RequestContext(request,datos))

def getPaquetes(request):
    dic={}
    datos={}
    datos['letrero']=''
    listaEncontrados=[]

    if request.is_ajax():
        if request.POST:
            getDatos(dic,request)
            precioMetodo={}
            formasEncontradas={}
            categoriasFormas={}
            estado=request.POST['estado']
            zonaEncontrada=''
            metodosImagenes={}
            bandera=False
            categoriasTotales=[]
            
        
            
            try:
                zonas=Zonas.objects.get(tienda=dic['tienda'],activo=1,estados__contains=estado)
                test=''
                zonaEncontrada=str(zonas.idzonas)
                bandera=True
                conector=connection.cursor()
                conector.execute('Select * from Paquetes_Formaenvio where Zonas='+zonaEncontrada+' and Activo=1 order by FormaEnvio')

                pfe=conector.fetchall()
                paquete={}
                for p in pfe:
                    banderaMetodo=True
                    
                    categoriasEncontradas=[]
                    categoriasTotales=[]
                    Contadorpaquetes={}
                    contador=0
                    paquete=Paquetes.objects.get(idpaquetes=str(p[0]))
                    formaenvio=Formaenvio.objects.get(idformaenvio=str(p[1]))
                    categorias=PaquetesCategorias.objects.raw('Select * from Paquetes_Categorias where Paquetes='+str(paquete.idpaquetes)+' and Activo=1')
                    cesta=request.session['modelos']
                    for c in categorias:        
                        for m in cesta:
                            productoEncontrado=str(m)
                            productoEncontrado=productoEncontrado.split(':')
                            productoEncontrado=productoEncontrado[0]
                            producto=Productos.objects.get(idproductos__exact=productoEncontrado)

                            if c.categorias == producto.categorias:
                                contador=contador+int(cesta[m])
                                listaEncontrados.append(str(producto.idproductos))
                                categoriasEncontradas.append(str(producto.categorias))


                            categoriasTotales.append(str(producto.categorias))

                    if categoriasFormas.get(str(formaenvio.nombre.encode('utf8')),False):
                        categoriasFormas[formaenvio.nombre.encode('utf8').encode('utf8')]+=categoriasEncontradas
                    else:
                        categoriasFormas[formaenvio.nombre.encode('utf8')]=categoriasEncontradas

                    if contador%(int(paquete.maximo)) != 0:
                        Contadorpaquetes[str(paquete.nombre.encode('utf8'))]=int(contador/int(paquete.maximo))+1
                    
                    else:
                        Contadorpaquetes[str(paquete.nombre.encode('utf8'))]=(contador/int(paquete.maximo))

                    metodosImagenes[formaenvio.nombre.encode('utf8')]=str(formaenvio.logo)

                    for cp in Contadorpaquetes:
                        if precioMetodo.get(str(formaenvio),False):
                            precioMetodo[str(formaenvio)]+=float(int(Contadorpaquetes[cp])*int(p[4]))
                        else:
                            precioMetodo[str(formaenvio)]=float(int(Contadorpaquetes[cp])*int(p[4]))

                    request.session['metodos']=precioMetodo

                for cf in categoriasFormas:
                    for c in categoriasTotales:
                        if not str(c) in categoriasFormas[cf]:
                            if precioMetodo.get(str(cf),False):
                                del precioMetodo[str(cf)]
                                del metodosImagenes[str(cf)]

                    

                for m in request.session['modelos']:
                    productoEncontrado=str(m)
                    productoEncontrado=productoEncontrado.split(':')
                    productoEncontrado=productoEncontrado[0]
                    producto=Productos.objects.get(idproductos=productoEncontrado)
                    if not productoEncontrado in listaEncontrados:
                        datos['Error']=True
                        datos['letrero']='<span class="icon-sad color-rojo"></span> Lo sentimos no hay envios para '+str(producto.categorias)+' a esa zona'
                

            except ObjectDoesNotExist:
                datos['Error']=True
                datos['letrero']='<span class="icon-sad color-rojo"></span> Lo sentimos no hay envios a esa zona'

            datos['datos']=json.dumps(precioMetodo)
            datos['metodos']=json.dumps(metodosImagenes)


        return HttpResponse(
                        json.dumps(datos),
                        content_type='application/json;charset=utf8')           
                    
    else:
        raise Http404

def quitarItem(request):
    dic={}
    cantidad=0;
    if request.is_ajax():
        if request.POST:
            try:
                existencias=0
                modelos=request.session['modelos']
                pro=str(request.POST['modelo'])
                pro=pro.split(':')
                try:
                    producto=Productos.objects.get(idproductos=pro[0])
                    modelo=Modelos.objects.get(idmodelos=pro[1])
                    if modelos.get(request.POST['modelo'],False):
                        del modelos[request.POST['modelo']]
                        request.session['modelos']=modelos
                        dic['Error']=False
                        dic['cesta']=getTotalCesta(request)
                    else:
                        dic['Error']=True
                        dic['cesta']=getTotalCesta(request)

                except ObjectDoesNotExist:
                    dic['Error']=True
                    dic['test']='No se encontro el objeto'
            except Exception, e:
                dic['test']='Oops! ocurrio un error'
                dic['Error']=True
        
        return HttpResponse(
                        json.dumps(dic),
                        content_type='application/json;charset=utf8')           
                    
    else:
        raise Http404

@transaction.atomic
def getTotal(request):
    dic={}
    datos={}
    pedido={}
    getDatos(datos,request)
    if request.is_ajax():
        if request.POST:
            total=request.session['total']
            if request.session.get('pedido',False):
                pedido      =request.session['pedido']
                dic['total']=float(pedido.importe)+float(pedido.importeenvio)
            else:
                metodo  = request.POST['metodo-envio']
                metodo  = metodo.split(':')
                metodo  = metodo[0]
                metodos = request.session['metodos']

                precioMetodo=float(metodos[metodo.encode('utf-8')])

                dic['total']=str(float(total)+precioMetodo)

                setPedido(request,datos,metodo,total,precioMetodo)

        return HttpResponse(
                        json.dumps(dic),
                        content_type='application/json;charset=utf8')           
                    
    else:
        raise Http404


@transaction.atomic
def setPedido(request,datos, metodo,total,precioMetodo):

    modelos                         = request.session['modelos']  
    pedido                          = Pedidos()
    pedido.clientes                 = request.session['idcliente']
    pedido.fecha                    = datetime.datetime.now()
    pedido.stock                    = datos['stock']
    pedido.activo                   = 1
    pedido.comentarios              = request.session['comentario']
    pedido.status                   = 'Pendiente'
    pedido.direccionenvio           = request.POST['direccion']+' '+request.POST['estado']
    pedido.estado                   = 1

    pedido.zonas                    = tienda.zonas_set.all().filter(activo=1,estados__contains=request.POST['estado'])
    request.session['formapago']    = Formapago.objects.get(nombre__exact=request.POST['formaPago'])
    #pedido.formapago=Formapago.objects.get(nombre__exact=request.POST['formaPago'])
    pedido.cpe                      = request.POST['cp']
    pedido.formaenvio               = Formaenvio.objects.get(nombre=metodo)
    pedido.importe                  = total
    pedido.importeenvio             = float(precioMetodo)
    pedido.save()
    request.session['pedido']       = pedido
    conexion = connection.cursor()
    #se le asigna una sesion al pedido
    request.session['pedido']       = pedido

    for p in modelos:
        pro         = str(p)
        pro         = pro.split(':')
        prod        = pro[0]
        modelo      = pro[1]
        producto    = Productos.objects.get(idproductos=prod)
        modelo      = Modelos.objects.get(idmodelos=modelo)
        cantidad    = getCesta(request,pro[1])
        #se asigna la cantidad de estock antes de el registro en el carrito
    

        #se valida si las existencias son mayores a la cantidad que se intenta introducir
        if (int(modelo.existencias)>=int(cantidad)):
            modelo.existencias=int(modelo.existencias)-int(cantidad)
            modelo.save()
            query='Insert Into Pedidos_Productos(Pedidos,Productos,Modelos,Cantidad,Activo) Values ('+str(pedido.idpedidos)+','+str(producto.idproductos)+','+str(modelo.idmodelos)+','+str(cantidad)+',1)'

            conexion.execute(query)
            try:
                transaction.commit_unless_managed()
            except DatabaseError, IntegrityError:
                getErrorLabel(True,dic)

            """producto.save()
            pp=PedidosProductos()
            pp.pedidos=pedido
            pp.productos=producto
            pp.modelos=modelo
            pp.cantidad=int(cantidadCesta)
            pp.activo=1
            pp.save()"""
        else:
            pp=PedidosProductos.objects.all().filter(pedidos=pedido)
            for p in pp:
                p.delete()
            pedido.delete()

            dic['Error']=True
            dic['test']='Existencias Insuficientes al realizar pedido intenta de nuevo'

    conexion.close()
    request.session['modelos']={}
    request.session['comentario']=''
    request.session['total']=0
    request.session['metodos']=[]
                

@transaction.atomic
def setPago(request):
    dic={}
    if request.is_ajax():
        if request.POST:

            pago=request.POST['amount']
            if float(pago)>= float(request.session['total'])/100:
                pedido          =request.session['pedido']
                pedido.status   ='Pagado'
                pedido.save()
                try:
                    cargo           =Cargos.objects.get(pedidos=pedido)
                    cargo.status    ='A'
                    cargo.save()
                except ObjectDoesNotExist:
                    cargo           = Cargos()
                    cargo.idcargo   = pedido.idpedidos
                    cargo.fecha     = datetime.datetime.now()
                    cargo.status    = 'A'
                    cargo.importe   = float(pedido.importe)+float(pedido.importeenvio)
                    cargo.formapago = request.session['formapago']
                    cargo.pedidos   = pedido
                    cargo.activo    = 1
                    cargo.save()
                    
                dic['status']='Pagado'  
                del request.session['pedido']

        return HttpResponse(
                        json.dumps(dic),
                        content_type='application/json;charset=utf8')           
                    
    else:
        raise Http404

def setPagoError(request):
    dic={}
    if request.is_ajax():
        if request.POST:
            pedido=request.session['pedido']
            pp=PedidosProductos.objects.all().filter(pedidos=pedido)
            for p in pp:
                modelo=Modelos.objects.get(idmodelos=p.modelos.idmodelos)
                modelo.existencias=int(modelo.existencias)+int(p.cantidad) 
                modelo.save()               
                p.delete()
            pedido.delete()
      
            del request.session['pedido']

        return HttpResponse(
                        json.dumps(dic),
                        content_type='application/json;charset=utf8')           
                    
    else:
        raise Http404

@transaction.atomic
def pagoOxxo(request):
    datos={}
    #getDatos(datos,request)
    if request.POST:
        response                        = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="Orden de Pago OXXO.pdf"'
        pedido                          = request.session['pedido']
        datos['code']                   = request.POST['numero']
        datos['url']                    = request.POST['url']
        datos['nip']                    = pedido.idpedidos
        datos['total']                  = float(pedido.importe)+float(pedido.importeenvio)
        datos['tienda']                 = Tienda.objects.get(site_id=settings.SITE_ID)

        pedido                          = request.session['pedido']

        cargo                           = Cargos()
        cargo.idcargo                  = request.POST['idcargo']
        cargo.fecha                     = datetime.datetime.now()
        cargo.status                    = 'P'
        cargo.importe                   = float(pedido.importe)+float(pedido.importeenvio)
        cargo.formapago                 = request.session['formapago']
        cargo.pedidos                   = pedido
        cargo.activo                    =  1
        cargo.save()
        #referencia de numero--------------------------
        referencia                      = Referencia()
        referencia.nombre               = 'numeroCodigo'
        referencia.valor                = request.POST['numero']
        referencia.cargos               = cargo
        referencia.save()
        #referencia url--------------------------------

        referencia                      = Referencia()
        referencia.nombre               = 'url'
        referencia.valor                = request.POST['url']
        referencia.cargos               = cargo
        referencia.save()

        p = fun.pagoOxxo(response,datos)
        #return render_to_response('plantilla1/oxxo.html',context_instance=RequestContext(request,datos))
        del request.session['pedido']
                
        return response

    else:
        raise Http404

@transaction.atomic
def pagoBanco(request):
    datos={}
    #getDatos(datos,request)
    if request.POST:
        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'filename="Orden de Pago BANORTE.pdf"'
        pedido                          = request.session['pedido']
        datos['banco']                  = request.POST['banco']
        datos['referencia']             = request.POST['referencia']
        datos['nip']                    = pedido.idpedidos
        datos['total']                  = float(pedido.importe)+float(pedido.importeenvio)
        datos['tienda']                 = Tienda.objects.get(site_id=settings.SITE_ID)
        #print pedido.idpedidos
        cargo                           = Cargos()
        cargo.idcargo                   = request.POST['idcargo']
        cargo.fecha                     = datetime.datetime.now()
        cargo.status                    = 'P'
        cargo.importe                   = float(pedido.importe)+float(pedido.importeenvio)
        cargo.formapago                 = request.session['formapago']
        cargo.pedidos                   = pedido
        cargo.activo                    = 1
        cargo.save()

        #referencia de numero--------------------------

        referencia                      = Referencia()
        referencia.nombre               = 'referencia'
        referencia.valor                = request.POST['referencia']
        referencia.cargos               = cargo
        referencia.save()
        #referencia url--------------------------------

        referencia                      = Referencia()
        referencia.nombre               = 'banco'
        referencia.valor                = request.POST['banco']
        referencia.cargos               = cargo
        referencia.save()

        p = fun.pagoBanco(response,datos)
        del request.session['pedido']
        return response

    else:
        raise Http404

def getCesta(request,prod):
    cantidad=0
    if request.session.get('modelos', False):
        modelos=request.session['modelos']
        for m in modelos:
            modeloEncontrado=str(m)
            modeloEncontrado=modeloEncontrado.split(':')
            modeloEncontrado=modeloEncontrado[1]
            if modeloEncontrado == prod:
                cantidad+=modelos[m]
    return cantidad

def getTotalCesta(request):
    cesta=0
    if request.session.get('modelos', False):
        modelos=request.session['modelos']
        for m in modelos:
            cesta+=modelos[m]
    return cesta

def Categoria(request,categoriaNombre):
    datos={}
    getDatos(datos,request)
    try:
        categoria=Categorias.objects.get(slug=categoriaNombre,stock=datos['stock'],activo=1)

        datos['categoria']=categoria.nombre
        productos=Productos.objects.all().extra(select={'nombre':'Productos.Nombre','archivo':'Galeria.archivo'}).filter(galeria__tipo="A").filter(categorias=categoria).filter(activo=1).order_by('-idproductos').filter(activo=1).distinct()

        print productos

        paginator = Paginator(productos, 16)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            fp = paginator.page(page)
        except (EmptyPage, InvalidPage):
            fp = paginator.page(paginator.num_pages)

        datos['productos']=fp

    except Exception, e:
        raise Http404



        

    return render_to_response('plantilla1/categorias.html',context_instance=RequestContext(request,datos))

def Busqueda(request):
    datos={}
    getDatos(datos,request)
    if request.POST:
        productos=Productos.objects.all().extra(select={'nombre':'Productos.Nombre','archivo':'Galeria.Archivo'}).filter(galeria__tipo="A").filter(categorias__in=datos['categorias']).filter(nombre__contains=request.POST['busqueda']).filter(activo=1).order_by('-idproductos').filter(activo=1).distinct()

        paginator = Paginator(productos, 16)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try:
            fp = paginator.page(page)
        except (EmptyPage, InvalidPage):
            fp = paginator.page(paginator.num_pages)

        datos['productos']=fp
    datos['categoria']='Resultados de '+request.POST['busqueda']

    return render_to_response('plantilla1/categorias.html',context_instance=RequestContext(request,datos))
#sdfasd
def allProducts(request):
    datos={}
    getDatos(datos,request)

    productos=Productos.objects.all().extra(select={'nombre':'Productos.Nombre','archivo':'Galeria.Archivo'}).filter(galeria__tipo="A").filter(categorias__in=datos['categorias']).order_by('-idproductos').filter(activo=1).distinct()

    paginator = Paginator(productos, 16)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        fp = paginator.page(page)
    except (EmptyPage, InvalidPage):
        fp = paginator.page(paginator.num_pages)

    datos['productos']=fp
    datos['categoria']=''

    return render_to_response('plantilla1/categorias.html',context_instance=RequestContext(request,datos))

def Contacto(request):
    datos={}
    getDatos(datos,request)

    return render_to_response('plantilla1/contacto.html',context_instance=RequestContext(request,datos))

def getDatos(dic,request):

    request.session.set_expiry(0)
    tienda                      = Tienda.objects.get(site_id=settings.SITE_ID)
    request.session['tienda']   = tienda
    stock                       = tienda.stock_set.get()
    categorias                  = stock.categorias_set.all().filter(activo=1)

    conjunto                    = Conjunto.objects.get(tienda__exact=tienda.idtienda)
    secciones                   = conjunto.secciones_set.all()

    pie                         = secciones.filter(nombre = 'Pie').get()
    cabecera                    = secciones.filter(nombre = 'Cabecera').get()

    dic['cesta']                = getTotalCesta(request)
    dic['template']             = 1
    dic['pie']                  = pie.contenido
    dic['cabecera']             = cabecera.contenido
    dic['logo']                 = tienda.logo
    dic['categorias']           = categorias
    dic['tienda']               = tienda
    dic['stock']                = stock
    dic['descripcionTienda']    = stripjs(tienda.descripcion)
    dic['Titulo']               = tienda.nombre

    dic['sesion']               = 'false'

    if request.session.get('clienteTienda',False):

        if request.session['clienteTienda']==False:
            dic['sesion']='false'
        else:
            dic['sesion']='true'

    if request.session.get('pedido',False):
        conexion    = connection.cursor()
        pedido      = request.session['pedido']
        conexion.execute('call borrarPedido('+str(pedido.idpedidos)+')')
        conexion.close()
        del request.session['pedido']


    propiedad = Propiedades.objects.all().filter(secciones__in=secciones)
    for p in propiedad:
        dic[p.nombre] = p.valor

def objetcUpdate(objeto,lista):
    listaObjeto=objeto.__dict__
    for atributo in listaObjeto:
        if atributo in lista:
            if atributo!='logo':
                objeto.__dict__[atributo]=lista[atributo]

def validarUser(request):
    if request.session.get('clienteTienda',False):
        if request.session["clienteTienda"]==False:
                return False
        else:
            return True
    else:
        return False

def validarCliente(user,password,tienda):
        try:
            Clientes.objects.get(mail=user,password=password,tienda=tienda)
            return True
        except ObjectDoesNotExist:
            return False

@csrf_exempt
def cancelarPedido(request):
    if request.is_ajax():
        if request.POST:
            dic={}
            conexion = connection.cursor()
            try:

                pedido  =   request.POST['idpedido']
                tienda  =   Tienda.objects.get(site_id=settings.SITE_ID)
                stock   =   tienda.stock_set.get()

                #Pedidos.objects.get(idpedidos=str(pedido),stock=stock)
                conexion.execute('call borrarPedido('+str(pedido)+')')
                try:
                    transaction.commit_unless_managed()
                except DatabaseError, IntegrityError:
                    getErrorLabel(True,dic)
                    conexion.close()    
               
                dic['Error']='false'
            except ObjectDoesNotExist:
                dic['Error']='true'

            return HttpResponse(
                        json.dumps(dic),
                        content_type='application/json;charset=utf8')           
                    
    else:
        raise Http404            

@csrf_exempt
def setData(request):
    dic={}
    pedidoRegresado={}
    
    if request.is_ajax():
        if request.POST:

            pedido                          = Pedidos.objects.get(idpedidos=request.POST['idpedido'])
            cargo                           = pedido.cargos_set.get()

            productos                       = PedidosProductos.objects.filter(pedidos=pedido,activo=1)

            pedidoRegresado['direccion']    = pedido.direccionenvio
            pedidoRegresado['cp']           = pedido.cpe
            pedidoRegresado['importe']      = str(pedido.importe+pedido.importeenvio)
            pedidoRegresado['metodoPago']   = cargo.formapago.nombre
            pedidoRegresado['metodoEnvio']  = pedido.formaenvio.nombre
            pedidoRegresado['precioMetodo'] = str(pedido.importeenvio)
            pedidoRegresado['status']       = pedido.status

            if request.session.get('pedidoCargo',False):
                del request.session['pedidoCargo']

            request.session['pedidoCargo']=str(pedido.idpedidos)
            
            productosRetornados={}

            for p in productos:
                auxiliar                    = {}
                auxiliar['modelo']          = str(p.modelos)
                auxiliar['precioModelo']    = str(p.modelos.precio)
                auxiliar['producto']        = str(p.productos.nombre)
                auxiliar['precioProducto']  = str(p.productos.precio)
                auxiliar['cantidad']        = str(p.cantidad)

                productosRetornados[str(p.pedidos.idpedidos)+str(p.productos)+str(p.modelos)]=auxiliar


            pedidoRegresado['productos']= json.dumps(productosRetornados)

            dic['pedido']               = pedido

        return HttpResponse(
                        json.dumps(pedidoRegresado),
                        content_type='application/json;charset=utf8')           
                    
    else:
        raise Http404

def salir(request):
    request.session["clienteTienda"]=False
    return HttpResponseRedirect('/')

def getCargo(request):
    import conekta

    llaves=TiendaFormapago.objects.get(tienda=Tienda.objects.get(site_id=settings.SITE_ID),formapago__exact='Conekta')

    conekta.api_version = "0.3.0"

    conekta.api_key = llaves.llaveprivada
    pedido=request.session['pedidoCargo']
    cargo=Cargos.objects.get(pedidos=str(pedido))

    charge = conekta.Charge.get(str(cargo.idcargo))
    monto= float(charge['amount'])/100
    metodo=charge['payment_method']
    forma= metodo['object']
    response = HttpResponse(content_type='application/pdf')
    datos={}
    if forma == 'bank_transfer_payment':
        response['Content-Disposition'] = 'filename="Orden de Pago BANORTE.pdf"'
        

        datos['banco']='BANORTE'
        datos['referencia']=metodo['reference']
        datos['nip']=pedido
        datos['total']=float(charge['amount'])/100
        datos['tienda']=Tienda.objects.get(site_id=settings.SITE_ID)

        """data = urllib.urlencode({"id": "51cef9faf23668b1f4000001", 
                                "created_at": 1395877725, 
                                "livemode": True, 
                                "type": "charge.paid",
                                "data": {
                                    "object": {
                                                "id":"51d5ea80db49596aa9000001",
                                                "created_at": '1395877725',
                                                'amount':'',
                                                'fee':'',
                                                "currency":"MXN",
                                                "status":"paid",
                                                'livemode':'',
                                                "description":"E-Book: Les Miserables",
                                                'error':'',
                                                'error_message':'',
                                                "payment_method":{
                                                "object":"card_payment",
                                                "last4":"1111",
                                                "name":"Arturo Octavio Ortiz"
                                            }
                                },
                                "previous_attributes": {
                                }
                                }
                                })

        datos={}
        req = urllib2.Request("http://wido.mx/webhook/", data)
        response = urllib2.urlopen(req)
        print response"""


        p = fun.pagoBanco(response,datos)
        
    else:
        response['Content-Disposition'] = 'filename="Orden de Pago OXXO.pdf"'
        datos['code']=metodo['barcode']
        datos['url']=metodo['barcode_url']
        datos['nip']=pedido
        datos['total']=float(charge['amount'])/100
        datos['tienda']=Tienda.objects.get(site_id=settings.SITE_ID)
        p = fun.pagoOxxo(response,datos)

    return response


from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
  #pagina principal-----------------------------------------
    url(r'^yopi/', 'admin.views.yopi', name='yopi'),
    url(r'^yopiRegister/', 'admin.views.yopiRegister', name='yopiRegister'),

    url(r'^$', 'admin.views.home', name='home'),
    url(r'^registrar/$','admin.views.registroUsuarios',name='registrar'),
    url(r'^articulo/$','admin.views.blog',name='blog'),
    url(r'^clientes/$','admin.views.clientes',name='client'),
    url(r'^ingresar/*([A-Za-z]+)/$','admin.views.login',name='login'),
    url(r'^registro/$','admin.views.registro',name='logar'),
    url(r'^verificar/$','cms.views.login',name='verify'),
    url(r'^correo/$','admin.views.contacto',name='contacto'),
    url(r'^Planes/$','admin.views.planes',name='planes'),
    url(r'^terminos/$','admin.views.terminos',name='planes'),
    url(r'^Galeria/$','admin.views.Galeria',name='galeria'),
    url(r'^crearTienda/$','admin.views.crearTienda',name='crearTienda'),
    url(r'^mitienda/$','admin.views.Curso',name='curso'),
    url(r'^correoContacto/$','admin.views.Correo',name='correoContacto'),
    url(r'^registroCurso/$','admin.views.registroCurso',name='rc'),
    
  #fin pagina principal----------------------------------------


   #panel de administracion---------------------------
   
    url(r'^pedido/(\d+)/$','cms.views.detallePedido',name='+pe'),
    url(r'^User/$','cms.views.User',name='Usuario'),
    url(r'^Completar/$','cms.views.Completar',name='completar'),
    url(r'^producto/nuevo/$','cms.views.addProduct',name='+p'),
    url(r'^producto/(\d+)/$','cms.views.modifyProduct',name='mp'),
    url(r'^productos/$','cms.views.listProducts',name='lp'),
    url(r'^categoria/nueva/$','cms.views.addCategory',name='+c'),
    url(r'^categoria/(\d+)/$','cms.views.modifyCategory',name='mc'),
    url(r'^categorias/$','cms.views.listCategory',name='lc'),
    url(r'^envios/$','cms.views.addSendForm',name='+e'),
    url(r'^metodo/nuevo/$','cms.views.addMetodo',name='+m'),
    url(r'^metodoE/$','cms.views.addMetodoE',name='+me'),
    url(r'^zona/nuevo/$','cms.views.addZone',name='+z'),
    url(r'^pedidosPanel/*([A-Za-z]+)/$','cms.views.adminArea',name='admin'),
    url(r'^paquetes/nuevo/(\d+)/$','cms.views.paquetesAdd',name='+paquetes'),
    url(r'^paquetes/(\d+)/$','cms.views.paquetes',name='paquetes'),
    url(r'^paquetes/(\d+)/(\d+)/$','cms.views.paquetesModify',name='paquetesModify'),

    url(r'^pasarelas/$','cms.views.pasarelas',name='admin'),

    url(r'^clientesTienda/$','cms.views.clientesTienda',name='clientes'),

    url(r'^addUnidad/$','cms.views.addUnit',name='+u'),
    url(r'^Anuncio/nuevo/$','cms.views.addAnuncio',name='+a'),
    url(r'^Anuncios/$','cms.views.anunciosList',name='la'),
    url(r'^Tienda/$','cms.views.miTienda',name='la'),
    url(r'^miEstilo/$','cms.views.Editor',name='+e'),
    url(r'^proximamente/*([A-Za-z]+)/$','cms.views.prox',name='+p'),

    url(r'^Eliminar/$','cms.views.eliminar',name='-i'),
    url(r'^Salir/$','cms.views.salir',name='salir'),

    url(r'^webhook/$','cms.views.Confirmar',name='Confirmar'),




   #fin panel------------------------------------------


   #plantillas------------------------------------------


   url(r'^tienda/$','store.views.home',name='hometiendas'),
   url(r'^ProductosTienda/(\d+)/$','store.views.articulo',name='articulo'),
   url(r'^Armar/$','store.views.setCarrito',name='+carrito'),
   url(r'^Desarmar/$','store.views.quitarItem',name='+carrito'),
   url(r'^Carrito/$','store.views.Carrito',name='carrito'),
   url(r'^Categorias/([\w-]+)/$','store.views.Categoria',name='categorias'),
   url(r'^Productos/$','store.views.allProducts',name='productos+'),
   url(r'^Busqueda/$','store.views.Busqueda',name='buscar'),
   url(r'^Contacto/$','store.views.Contacto',name='contacto'),
   url(r'^Registro/$','store.views.registroClientes',name='registro'),
   url(r'^ClienteLogin/$','store.views.loginCliente',name='loginC'),
   url(r'^Procesar/$','store.views.Procesar',name='procesar'),
   url(r'^panelUsuario/$','store.views.panelUser',name='panelUser'),
   url(r'^costoPaquete/$','store.views.getPaquetes',name='panelUser'),
   url(r'^Total/$','store.views.getTotal',name='total'),
   url(r'^reportar/$','store.views.setPago',name='reporte'),
   url(r'^reportarError/$','store.views.setPagoError',name='reporte'),

   url(r'^pagoOxxo/$','store.views.pagoOxxo',name='oxxo'),
   url(r'^pagoBanco/$','store.views.pagoBanco',name='oxxo'),
   url(r'^getData/$','store.views.setData',name='data'),
   url(r'^CorreoTienda/$','store.views.Correo',name='mail'),
   url(r'^SalirUser/$','store.views.salir',name='salirU'),
   url(r'^borrarPedido/$','store.views.cancelarPedido',name='-pe'),
   url(r'^Cargo/$','store.views.getCargo',name='cargo'),
   url(r'^Clave/$','store.views.setPass',name='clave'),



   #fin plantillas--------------------------------------

   # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

handler404 = 'admin.views.error404'

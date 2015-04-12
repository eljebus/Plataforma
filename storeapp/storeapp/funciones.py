# -*- coding: utf-8 -*-
from django.core.paginator import *
from django.templatetags.static import static
import StringIO

import httplib, ssl, urllib2, socket

class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)
        
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
        except ssl.SSLError, e:
            print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
            
class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)

# install opener

urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))


class Funciones():
	def validarForm(self,formulario):
		valor={"vacio":False,"valores":''}
		for clave in formulario:
			if(clave!='logo' and clave!='files[]'):
				if(len(formulario[clave])==0):
					
					valor['vacio']=True
					valor['valores']+=clave+" "

		return valor
		from django.core.paginator import ObjectPaginator, InvalidPage

	def pagoOxxo(self,response,datos):
		import reportlab
		from reportlab.pdfgen import canvas
		from reportlab.graphics.shapes import *
		from reportlab.graphics import renderPDF
		from reportlab.rl_config import defaultPageSize
		import PIL
		PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]

		tienda=datos['tienda']
		p = canvas.Canvas(response)	
		#p.drawImage('http://www.mindoncloud.com/images/logo.png',60,740,150,80,mask='auto')
		#p.drawImage(static(str(tienda.logo)),60,740,150,80,mask='auto')
		p.setFont('Times-Bold',16)
		p.drawString(270,750,str(tienda.nombre))
		p.drawString(60,700, "Pago en OXXO")
		p.setFont('Courier',16)
		p.drawString(60,680, "Numero de Pedido "+str(datos['nip']))
		p.drawString(60,660, "Monto a Pagar $ "+str(datos['total']))
		p.setFont('Courier',12)
		p.drawString(60,630,'La compra se encuentra en estado Pendiente.')
		p.drawString(60,613,'Imprime y presenta este comprobante en cualquier tienda OXXO del país')
		p.drawString(60,600,'para realizar el pago por tu compra.')
		p.drawString(60,583,'El presente recibo solo es valido para el pago que estas efectuando')
		p.drawString(60,571,'y recuerda que se acreditará en Ia cuenta del vendedor a las 24 hs.')
		p.drawString(60,554,'Cualquier aclaración sobre tu compra comunícate con tu vendedor')
		p.drawImage('http://www.durango.gob.mx/img/29467/oxxo-01.png',(PAGE_WIDTH/2.0)-85,450,150,80,mask='auto')
		
		

		import cStringIO
		import io
		import PIL.Image
		from reportlab.lib.utils import ImageReader
        
		
		fd = urllib2.urlopen(datos['url'])
		image_file = StringIO.StringIO(fd.read())
		im = PIL.Image.open(image_file)
		im = ImageReader(im)

		#p.drawImage(im,PAGE_WIDTH/2.0-80,430,150,80,mask='auto')
		
		#p.drawImage(datos['url'],PAGE_WIDTH/2.0-120,380,mask='auto')

		#p.drawString(datos['url'])
		p.drawImage(im,PAGE_WIDTH/2.0-122,380,245)
		#p.drawImage('https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Code_128B-2009-06-02.svg/500px-Code_128B-2009-06-02.svg.png',PAGE_WIDTH/2.0-120,380)

		p.drawCentredString(PAGE_WIDTH/2.0,370,str(datos['code']))

		p.drawString(60,330,'(*) El presente recibo debe imprimirse de forma legible y clara,')
		#p.drawString(60,350,datos['url'])
		p.drawString(60,317,'preferentemente con impresora láser y conservarse en buen estado sin')
		p.drawString(60,304,'tachaduras y/o dobleces. De lo contrario, puede que la tienda donde ')
		p.drawString(60,291,'intentes efectuar tu pago, no pueda capturarlo.')


		p.showPage()
		p.save()

		return p

	def pagoBanco(self,response,datos):

		from reportlab.pdfgen import canvas
		from reportlab.graphics.shapes import *
		from reportlab.graphics import renderPDF
		from reportlab.rl_config import defaultPageSize
		PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
		tienda=datos['tienda']
		p = canvas.Canvas(response)	
		p.drawImage('http://soundsystems.com.mx/wp-content/uploads/2013/12/banorte-logo.jpg',(PAGE_WIDTH/2.0)-85,450,150,80,mask='auto')
		#p.drawImage(static(str(tienda.logo)),60,740,150,80,mask='auto')
		p.setFont('Times-Bold',16)
		p.drawString(270,750,str(tienda.nombre))
		p.drawString(60,700, "Deposito Bancario")
		p.setFont('Courier',16)
		p.drawString(60,680, "Numero de Pedido "+str(datos['nip']))
		p.drawString(60,660, "Monto a Pagar $ "+str(datos['total']))
		p.setFont('Courier',12)
		p.drawString(60,630,'La compra se encuentra en estado Pendiente.')

		p.drawString(60,583,'El presente recibo solo es válido para el pago que estas efectuando')
		p.drawString(60,571,'y recuerda que se acreditará en Ia cuenta del vendedor a las 24 hs.')
		p.drawString(60,554,'Cualquier aclaración sobre tu compra comunícate con tu vendedor')

		

		p.drawString(PAGE_WIDTH/2.0-70,415,' Banco: '+str(datos['banco']) ) 
		p.drawCentredString(PAGE_WIDTH/2.0,400,'Referencia: '+str(datos['referencia']))

		p.drawString(60,330,'(*) El presente recibo debe imprimirse de forma legible y clara,')
		p.drawString(60,317,'preferentemente con impresora láser y conservarse en buen estado sin')
		p.drawString(60,304,'tachaduras y/o dobleces. De lo contrario, puede que la tienda donde ')
		p.drawString(60,291,'intentes efectuar tu pago, no pueda capturarlo.')


		p.showPage()
		p.save()

		return p

	